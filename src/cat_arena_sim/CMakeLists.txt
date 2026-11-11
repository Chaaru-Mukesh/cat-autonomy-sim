cmake_minimum_required(VERSION 3.8)
project(cat_arena_sim)

find_package(ament_cmake REQUIRED)

install(DIRECTORY worlds models
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS scripts/generate_heightmap.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
