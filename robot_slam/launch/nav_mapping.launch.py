import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'robot_slam'
    package_dir = get_package_share_directory(package_name)
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    nav2_yaml = os.path.join(package_dir, 'config', 'nav2_params.yaml')
    
    controller_yaml = os.path.join(package_dir, 'config', 'controller.yaml')
    bt_navigator_yaml = os.path.join(package_dir, 'config', 'bt_navigator.yaml')
    planner_yaml = os.path.join(package_dir, 'config', 'planner_server.yaml')
    behavior_yaml = os.path.join(package_dir, 'config', 'behavior.yaml')

    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_yaml, {'use_sim_time': use_sim_time}],
        remappings=[('cmd_vel', '/diff_cont/cmd_vel_unstamped')]
    )

    planner_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_yaml, {'use_sim_time': use_sim_time}]
    )

    behavior_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_yaml, {'use_sim_time': use_sim_time}]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_yaml, {'use_sim_time': use_sim_time}]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': True},
            {'node_names': ['controller_server',
                           'planner_server',
                           'behavior_server',
                           'bt_navigator']}
        ]
    )

    return LaunchDescription([
        declare_use_sim_time,
        controller_node,
        planner_node,
        behavior_node,
        bt_navigator_node,
        lifecycle_manager_node
    ])