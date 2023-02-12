import os

from ament_index_python.packages import get_package_share_directory

import launch
import launch_ros.actions


def generate_launch_description():
    joy_config = launch.substitutions.LaunchConfiguration('joy_config')
    joy_dev = launch.substitutions.LaunchConfiguration('joy_dev')
    config_filepath = launch.substitutions.LaunchConfiguration('config_filepath')

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument('joy_vel', default_value='cmd_vel'),
        launch.actions.DeclareLaunchArgument('joy_config', default_value='gamepad'),
        launch.actions.DeclareLaunchArgument('joy_dev', default_value='/dev/input/js0'),
        launch.actions.DeclareLaunchArgument('config_filepath', default_value=[
            launch.substitutions.TextSubstitution(text=os.path.join(
                get_package_share_directory('my_robot_bringup'), 'config', '')),
            joy_config, launch.substitutions.TextSubstitution(text='.config.yaml')]),

        launch_ros.actions.Node(
            package='joy', 
            executable='joy_node', 
            name='joy_node',
            parameters=[
            	{
                	'dev': joy_dev,
	                'deadzone': 0.3,
        	        'autorepeat_rate': 20.0,
        	}
           ]
        ),
        launch_ros.actions.Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop_twist_joy_node', parameters=[config_filepath]
        ),

    	launch_ros.actions.Node(
                package='hoverboard-driver-pkg',
                executable='hoverboard-driver',
                name='hoverboard_driver_node',
                parameters=[
                    {
                        'x_kp': 800.0,
                        'x_kd': 1.0,
                        'x_kff': 280.0,
                        'x_d_alpha': 0.1,
                        'x_o_alpha': 0.05,
                        'w_kp': 200.0,
                        'w_kd': 0.0,
                        'w_kff': 280.0,
                        'w_d_alpha': 0.1,
                        'w_o_alpha': 0.05,
                    }
                ]
	   ),            
    ])
