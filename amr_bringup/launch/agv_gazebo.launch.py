import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory , get_package_share_path
from launch.substitutions import Command
from launch.actions import ExecuteProcess

def generate_launch_description():

    urdf_path = os.path.join(get_package_share_directory('amr_description'),
                                                    'urdf',
                                                    'my_robot.urdf.xacro')
    
    # rviz_path = os.path.join(get_package_share_path('amr_description'),
    #                                                 'rviz',
    #                                                 'urdf_config.rviz')

    world = os.path.join(get_package_share_directory('amr_bringup'),
                                                    'worlds',
                                                    'gz_world.sdf')
    
    bridge_path = os.path.join(get_package_share_directory('amr_bringup'),
                                                            'config',
                                                            'gazebo_bridge.yaml')
    
    robot_description = ParameterValue(Command(['xacro ' , urdf_path]), value_type=str)
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    gz_sim_launch = ExecuteProcess(             #this node launches the gazebo sim with gz_world.sdf file 
        cmd=['gz', 'sim', '-r', '-v 4', world],
        output="screen"
    )
    
    amr_spawn_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', 'robot_description']
    )

    gz_bridge_launch_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_path}',
        ],
        output="screen",
    )

    # rviz2_launch_node = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     arguments=['-d', rviz_path]
    # )

    return LaunchDescription([
        robot_state_publisher_node,
        gz_sim_launch,
        amr_spawn_node,
        gz_bridge_launch_node,
        # rviz2_launch_node
    ])

