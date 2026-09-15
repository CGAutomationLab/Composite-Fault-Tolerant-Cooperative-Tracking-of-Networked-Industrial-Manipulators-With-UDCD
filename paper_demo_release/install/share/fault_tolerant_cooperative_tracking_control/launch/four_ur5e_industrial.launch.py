import os


from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    LogInfo,
    RegisterEventHandler,
    TimerAction,
)
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from ament_index_python.packages import (
    get_package_prefix,
    get_package_share_directory,
)

PACKAGE_NAME = "fault_tolerant_cooperative_tracking_control"


def create_robot_stack(
    robot_name: str,
    x: float,
    y: float,
    yaw: float,
    urdf_file: str,
    controllers_file: str,
    robot_mount_height: float,
):
    namespace = robot_name
    tf_prefix = f"{robot_name}_"
    controller_manager_name = f"/{namespace}/controller_manager"

    robot_description_content = Command(
        [
            FindExecutable(name="xacro"),
            " ",
            urdf_file,
            " ",
            "name:=", robot_name,
            " ",
            "ur_type:=ur5e",
            " ",
            "tf_prefix:=", tf_prefix,
            " ",
            "ros_namespace:=/", namespace,
            " ",
            "simulation_controllers:=", controllers_file,
            " ",
            "robot_mount_height:=", str(robot_mount_height),
            " ",
            "safety_limits:=true",
            " ",
            "safety_pos_margin:=0.15",
            " ",
            "safety_k_position:=20",
        ]
    )

    robot_description = {
        "robot_description": robot_description_content,
        "use_sim_time": True,
    }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=namespace,
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name=f"spawn_{robot_name}",
        output="screen",
        arguments=[
            "-string", robot_description_content,
            "-name", robot_name,
            "-x", str(x),
            "-y", str(y),
            "-z", "0.0",
            "-Y", str(yaw),
            "-allow_renaming", "false",
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name=f"spawner_joint_state_broadcaster_{robot_name}",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", controller_manager_name,
            "--controller-manager-timeout", "120",
        ],
    )

    effort_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        name=f"spawner_effort_controller_{robot_name}",
        output="screen",
        arguments=[
            "effort_controller",
            "--controller-manager", controller_manager_name,
            "--controller-manager-timeout", "120",
            "--inactive",
        ],
    )

    return {
        "name": robot_name,
        "rsp": robot_state_publisher,
        "spawn": spawn_robot,
        "jsb": joint_state_broadcaster_spawner,
        "effort": effort_controller_spawner,
    }


def generate_launch_description():
    package_share = get_package_share_directory(PACKAGE_NAME)

    urdf_file = os.path.join(
        package_share,
        "urdf",
        "ur5e_instance.urdf.xacro",
    )

    controllers_file = os.path.join(
        package_share,
        "config",
        "multi_ur_controllers.yaml",
    )



    package_prefix = get_package_prefix(
        PACKAGE_NAME
    )
    gz_ros2_control_prefix = get_package_prefix(
        "gz_ros2_control"
    )

    gz_ros2_control_lib = os.path.join(
        gz_ros2_control_prefix,
        "lib",
    )
    sealed_world_server = os.path.join(
        package_prefix,
        "lib",
        PACKAGE_NAME,
        "sealed_world_server",
    )
    gz_plugin_paths = [
        os.environ.get(
            "GZ_SIM_SYSTEM_PLUGIN_PATH",
            "",
        ),
        os.environ.get(
            "LD_LIBRARY_PATH",
            "",
        ),
        gz_ros2_control_lib,
    ]

    gz_plugin_path = os.pathsep.join(
        path
        for path in gz_plugin_paths
        if path
    )
    gazebo_server = ExecuteProcess(
        cmd=[
            sealed_world_server,
        ],
        output="screen",
        additional_env={
            "GZ_SIM_SYSTEM_PLUGIN_PATH":
                gz_plugin_path,
        },
    )
    gazebo_gui = ExecuteProcess(
        cmd=[
            "gz",
            "sim",
            "-g",
            "-v",
            "4",
        ],
        output="screen",
    )

    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="clock_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"
        ],
    )

    # Final one-line industrial workcell layout.
    robot_layout = [
        ("ur1", -3.60, -0.78, 1.5708),
        ("ur2", -1.20, -0.78, 1.5708),
        ("ur3",  1.20, -0.78, 1.5708),
        ("ur4",  3.60, -0.78, 1.5708),
    ]

    robot_mount_height = 0.95

    stacks = [
        create_robot_stack(
            robot_name=name,
            x=x,
            y=y,
            yaw=yaw,
            urdf_file=urdf_file,
            controllers_file=controllers_file,
            robot_mount_height=robot_mount_height,
        )
        for name, x, y, yaw in robot_layout
    ]

    actions = [
    gazebo_server,

    TimerAction(
        period=2.0,
        actions=[
            gazebo_gui,
        ],
    ),

    clock_bridge,

    LogInfo(
        msg=(
            "Embedded Gazebo industrial world is starting. "
            "Robot spawning will begin after a "
            "10 s stabilization delay."
        )
    ),
]

    # ----------------------------------------------------------------------
    # Robust sequential startup
    #
    # Previous version:
    #   UR1 / UR2 / UR3 / UR4 were fired by fixed timers at 2/4/6/8 s.
    #
    # Final version:
    #   wait for Gazebo -> UR1 -> JSB -> effort -> UR2 -> ... -> UR4
    #
    # This deliberately serializes the expensive robot / ros2_control startup
    # and avoids four controller_manager instances competing during world load.
    # ----------------------------------------------------------------------

    actions.append(
        TimerAction(
            period=10.0,
            actions=[
                LogInfo(msg="Starting UR1 (1/4)..."),
                stacks[0]["rsp"],
                stacks[0]["spawn"],
            ],
        )
    )

    for i, stack in enumerate(stacks):
        robot_name = stack["name"]

        # Robot entity created -> wait briefly -> load JointStateBroadcaster.
        actions.append(
            RegisterEventHandler(
                OnProcessExit(
                    target_action=stack["spawn"],
                    on_exit=[
                        LogInfo(
                            msg=(
                                f"{robot_name}: spawn process finished. "
                                "Waiting for its controller_manager..."
                            )
                        ),
                        TimerAction(
                            period=1.5,
                            actions=[stack["jsb"]],
                        ),
                    ],
                )
            )
        )

        # JointStateBroadcaster ready -> load effort controller INACTIVE.
        actions.append(
            RegisterEventHandler(
                OnProcessExit(
                    target_action=stack["jsb"],
                    on_exit=[
                        TimerAction(
                            period=0.8,
                            actions=[stack["effort"]],
                        ),
                    ],
                )
            )
        )

        # After this robot's effort controller is configured, proceed to the
        # next robot.  The final robot just prints a completion message.
        if i < len(stacks) - 1:
            next_stack = stacks[i + 1]
            actions.append(
                RegisterEventHandler(
                    OnProcessExit(
                        target_action=stack["effort"],
                        on_exit=[
                            LogInfo(
                                msg=(
                                    f"{robot_name}: ros2_control stack ready. "
                                    f"Starting {next_stack['name'].upper()} "
                                    f"({i + 2}/4)..."
                                )
                            ),
                            TimerAction(
                                period=0.8,
                                actions=[
                                    next_stack["rsp"],
                                    next_stack["spawn"],
                                ],
                            ),
                        ],
                    )
                )
            )
        else:
            actions.append(
                RegisterEventHandler(
                    OnProcessExit(
                        target_action=stack["effort"],
                        on_exit=[
                            LogInfo(
                                msg=(
                                    "ALL FOUR UR5e ROBOTS HAVE COMPLETED "
                                    "THE SEQUENTIAL SPAWN / CONTROLLER SETUP."
                                )
                            ),
                        ],
                    )
                )
            )

    return LaunchDescription(actions)
