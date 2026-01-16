# touch_telz.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare  # ✅ 正确导入（Humble）
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    # 包含 omni_common 的驱动 launch 文件
    omni_state_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('omni_common'),
                'launch',
                'omni_state.launch.py'
            ])
        ])
    )

    # 启动你的 trajectory_projector 节点
    projector_node = Node(
        package='touch_mapper',
        executable='trajectory_projector',
        name='trajectory_projector',
        output='screen',
        emulate_tty=True
    )

    return LaunchDescription([
        omni_state_launch,
        projector_node
    ])