from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


PACKAGE_NAME = "fault_tolerant_cooperative_tracking_control"

COMMON_START_TOPIC = "/cooperative_tracking/start"
READY_TOPIC_PREFIX = "/cooperative_tracking/tracker"


def generate_launch_description():
    inject_faults = LaunchConfiguration("inject_actuator_faults")
    inject_disturbance = LaunchConfiguration("inject_external_disturbance")

    # The effort controllers must already be ACTIVE before this launch is run.
    #
    # The barrier does NOT activate ros2_control controllers. It only synchronizes
    # the true V161 tracking start after all four tracking processes are ready.
    start_barrier = Node(
        package=PACKAGE_NAME,
        executable="cooperative_tracking_start_barrier",
        name="cooperative_tracking_start_barrier",
        output="screen",
        parameters=[
            {
                "start_topic": COMMON_START_TOPIC,
                "ready_topic_prefix": READY_TOPIC_PREFIX,
                "republish_period": 0.10,
            }
        ],
    )

    tracking_nodes = []

    for robot_id in range(1, 5):
        executable = (
            "fault_tolerant_pp_cooperative_tracking_control_with_delay_tracking"
            f"{robot_id}"
        )

        tracking_nodes.append(
            Node(
                package=PACKAGE_NAME,
                executable=executable,
                name=executable,
                output="screen",
                parameters=[
                    {
                        "use_sim_time": True,
                        "inject_actuator_faults": inject_faults,
                        "inject_external_disturbance": inject_disturbance,
                        "torque_limit": 100.0,
                        "fault_start_time": 8.0,

                        # Synchronization only. The validated V161 control law,
                        # gains and performance functions are unchanged.
                        "enable_cooperative_start_barrier": True,
                        "cooperative_ready_topic":
                            f"{READY_TOPIC_PREFIX}{robot_id}_ready",
                        "cooperative_start_topic": COMMON_START_TOPIC,
                    }
                ],
            )
        )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "inject_actuator_faults",
                default_value="true",
                description=(
                    "Apply the configured multiplicative and additive "
                    "actuator-fault model."
                ),
            ),
            DeclareLaunchArgument(
                "inject_external_disturbance",
                default_value="true",
                description=(
                    "Inject the configured bounded joint disturbance."
                ),
            ),
            LogInfo(
                msg=(
                    "Starting all four V161 tracking nodes directly. "
                    "No effort-controller activation or launch delay is performed here. "
                    "The common READY/START barrier will release all four tracking clocks together."
                )
            ),
            start_barrier,
            *tracking_nodes,
        ]
    )
