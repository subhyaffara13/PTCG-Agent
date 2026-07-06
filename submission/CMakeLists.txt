cmake_minimum_required(VERSION 3.12)
project(ptcg_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable FetchContent for auto-downloading pybind11 if not installed
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(ptcg_core
    src/bindings.cpp
    src/ptcg_simulator.cpp
    src/cpp_mcts.cpp
)

target_include_directories(ptcg_core PRIVATE src)
