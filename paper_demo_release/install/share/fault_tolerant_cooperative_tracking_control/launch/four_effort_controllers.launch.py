from launch import LaunchDescription
from launch.actions import ExecuteProcess, LogInfo


PACKAGE_NAME = "fault_tolerant_cooperative_tracking_control"


def generate_launch_description():
    activate_effort_process = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            PACKAGE_NAME,
            "activate_effort_controllers.sh",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            LogInfo(
                msg=(
                    "Activating the four UR5e effort controllers. "
                    "After all four are active, keep this Gazebo session running "
                    "and start four_tracking_controllers.launch.py in another terminal."
                )
            ),
            activate_effort_process,
        ]
    )
