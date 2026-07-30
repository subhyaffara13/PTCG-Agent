cmake_minimum_required(VERSION 3.12)
project(ptcg_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable FetchContent for auto-downloading pybind11 if not installed
include(FetchContent)
FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/tags/v2.11.1.zip
)
FetchContent_MakeAvailable(pybind11)

# Fetch ONNX Runtime prebuilt binaries
if(WIN32)
  set(ONNXRUNTIME_URL "https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip")
  set(ONNXRUNTIME_LINK_LIB "onnxruntime.lib")
  set(ONNXRUNTIME_SHARED_LIB "onnxruntime.dll")
else()
  set(ONNXRUNTIME_URL "https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-linux-x64-1.16.3.tgz")
  set(ONNXRUNTIME_LINK_LIB "libonnxruntime.so")
  set(ONNXRUNTIME_SHARED_LIB "libonnxruntime.so")
endif()

FetchContent_Declare(
  onnxruntime
  URL ${ONNXRUNTIME_URL}
)
FetchContent_MakeAvailable(onnxruntime)

pybind11_add_module(ptcg_core
    src/bindings.cpp
    src/ptcg_simulator.cpp
    src/cpp_mcts.cpp
)

target_include_directories(ptcg_core PRIVATE src ${onnxruntime_SOURCE_DIR}/include)
target_link_libraries(ptcg_core PRIVATE ${onnxruntime_SOURCE_DIR}/lib/${ONNXRUNTIME_LINK_LIB})

# Copy ONNX Runtime shared library next to output binary
add_custom_command(TARGET ptcg_core POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${onnxruntime_SOURCE_DIR}/lib/${ONNXRUNTIME_SHARED_LIB}"
    $<TARGET_FILE_DIR:ptcg_core>
)
