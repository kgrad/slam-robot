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
    map_file = LaunchConfiguration('map_file')
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    declare_map_file = DeclareLaunchArgument(
        'map_file',
        default_value='/home/robot-host/dev_ws/my_map.yaml',  # Updated absolute path
        description='Full path to map yaml file to load'
    )

    nav2_params_path = os.path.join(package_dir, 'config', 'nav2_params.yaml')
    amcl_params_path = os.path.join(package_dir, 'config', 'amcl.yaml')

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': '/home/robot-host/dev_ws/my_map.yaml'},  # Hardcoded correct path
                   {'use_sim_time': use_sim_time}]
    )

    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[amcl_params_path,
                   {'use_sim_time': use_sim_time,
                    'global_localization_random_yaw': True,  # Enable random yaw for global localization
                    'set_initial_pose': False,  # Don't require initial pose
                    'initial_pose': {
                        'x': 0.0,
                        'y': 0.0,
                        'z': 0.0,
                        'yaw': 0.0
                    }}],
        remappings=[('cmd_vel', '/diff_cont/cmd_vel_unstamped')]
    )

    # Include all navigation nodes
    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        parameters=[nav2_params_path],
        remappings=[('cmd_vel', '/diff_cont/cmd_vel_unstamped')]
    )

    planner_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    recoveries_node = Node(
        package='nav2_behaviors',  # Changed from nav2_recoveries
        executable='behavior_server',  # Changed from recoveries_server
        name='behavior_server',  # Changed from recoveries_server
        output='screen',
        parameters=[nav2_params_path]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params_path]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': True},
            {'node_names': ['map_server',
                           'amcl',
                           'controller_server',
                           'planner_server',
                           'behavior_server',  # Changed from recoveries_server
                           'bt_navigator']}
        ]
    )

    # Add RViz
    nav2_dir = get_package_share_directory('nav2_bringup')
    rviz_config_dir = os.path.join(nav2_dir, 'rviz', 'nav2_default_view.rviz')
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_map_file,
        map_server_node,
        amcl_node,
        controller_node,
        planner_node,
        recoveries_node,
        bt_navigator_node,
        lifecycle_manager_node,
        rviz_node  # Add rviz_node to the launch description
    ])