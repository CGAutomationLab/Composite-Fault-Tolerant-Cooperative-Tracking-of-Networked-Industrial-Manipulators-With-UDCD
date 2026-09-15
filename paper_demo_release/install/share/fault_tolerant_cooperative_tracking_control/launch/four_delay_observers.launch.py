from launch import LaunchDescription
from launch_ros.actions import Node


PACKAGE_NAME = "fault_tolerant_cooperative_tracking_control"


def generate_launch_description():
    nodes = []
    for index in range(1, 5):
        executable = (
            "fault_tolerant_pp_cooperative_tracking_control_with_delay_observer"
            f"{index}"
        )
        nodes.append(
            Node(
                package=PACKAGE_NAME,
                executable=executable,
                name=executable,
                output="screen",
                parameters=[{"use_sim_time": True}],
            )
        )
    return LaunchDescription(nodes)
