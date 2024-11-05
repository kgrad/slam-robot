cmake_minimum_required(VERSION 3.8)
project(model_lidar)

# Set the C++ standard to 17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Add compile options for warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -pedantic)
endif()

# Find dependencies manually
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_ros REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(rclcpp_components REQUIRED)

# Define RPLIDAR SDK path
set(RPLIDAR_SDK_PATH "./sdk/")

# Collect RPLIDAR SDK source files
file(GLOB RPLIDAR_SDK_SRC
  "${RPLIDAR_SDK_PATH}/src/arch/linux/*.cpp"
  "${RPLIDAR_SDK_PATH}/src/hal/*.cpp"
  "${RPLIDAR_SDK_PATH}/src/*.cpp"
)

# Include directories
include_directories(
  ${RPLIDAR_SDK_PATH}/include
  ${RPLIDAR_SDK_PATH}/src
  include
)

# Build the composition node as a shared library
add_library(rplidar_composition_node SHARED
  src/rplidar_node.cpp
  ${RPLIDAR_SDK_SRC}
)
ament_target_dependencies(rplidar_composition_node rclcpp sensor_msgs std_srvs rclcpp_components)
rclcpp_components_register_nodes(rplidar_composition_node "rplidar_ros::rplidar_node")

# Build standalone executable
add_executable(rplidar_composition src/standalone_rplidar.cpp)
target_link_libraries(rplidar_composition rplidar_composition_node)
ament_target_dependencies(rplidar_composition rclcpp sensor_msgs std_srvs rclcpp_components)

# Install executables and libraries
install(
  TARGETS rplidar_composition rplidar_composition_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# Install additional directories (launch, rviz, config, description, worlds)
install(
  DIRECTORY launch rviz config description worlds
  DESTINATION share/${PROJECT_NAME}
)

# Package export
ament_package()
