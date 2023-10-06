cmake_minimum_required(VERSION 3.0.0)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_TOOLCHAIN_FILE "/Users/wukun/workshop/Learn/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")
project(increase VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(increase main.cpp)
add_executable(heart heart.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

set(PYTHON_INCLUDE_DIRS ${PYTHON_INCLUDE_DIRS} "/Users/wukun/opt/anaconda3/include/python3.9")

# define WITHOUT_NUMPY so numpy header files are not necessary
add_compile_definitions(WITHOUT_NUMPY)
# set(PYTHON_INCLUDE_DIRS ${PYTHON_INCLUDE_DIRS} "/Users/wukun/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include")

find_path(MATPLOTLIB_CPP_INCLUDE_DIRS "matplotlibcpp.h")
target_include_directories(increase PRIVATE ${MATPLOTLIB_CPP_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
target_include_directories(heart PRIVATE ${MATPLOTLIB_CPP_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})

find_package(Python3 COMPONENTS Development REQUIRED)
target_link_libraries(increase PRIVATE Python3::Python)
target_link_libraries(heart PRIVATE Python3::Python)