cmake_minimum_required(VERSION 3.1)

project(seir C CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Boost REQUIRED)


add_executable(seir seir.cpp seir.h)

target_include_directories(seir PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${Boost_INCLUDE_DIRS}
    )
