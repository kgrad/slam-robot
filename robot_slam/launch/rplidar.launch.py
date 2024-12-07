from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os

def generate_launch_description():
    serial_port = '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4:1.0-port0'
    
    # Check if port exists
    if not os.path.exists(serial_port):
        return LaunchDescription([
            LogInfo(msg=f'Error: Serial port {serial_port} does not exist. Please check connection.')
        ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'serial_port',
            default_value=serial_port,
            description='RPLidar serial port'
        ),
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar_node',
            parameters=[{
                'serial_port': LaunchConfiguration('serial_port'),
                'serial_baudrate': 115200,
                'frame_id': 'lidar',
                'angle_compensate': True,
                'scan_mode': 'Standard',
                'publish_rate': 2.5,    # Reduced from 5.0
                'queue_size': 500,      # Reduced from 1000
                'scan_time': 0.1,
                'range_min': 0.15,
                'range_max': 12.0,
                'time_offset': 0.0,
                'angle_min': -3.14159,
                'angle_max': 3.14159,
                'ignore_array': '',
                'filter_samples': True
            }],
            output='screen'
        )
    ])
