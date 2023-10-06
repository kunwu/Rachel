需要配置vcpkg，并安装matplotlib-cpp，命令如下：
在一个公共目录下，例如workshop
git clone https://github.com/microsoft/vcpkg
cd vcpkg
./bootstrap-vcpkg.sh -disableMetrics
./vcpkg integrate zsh # 这一步是用来和当前的shell做集成，以支持自动补全等shell功能，可以不做
./vcpkg install matplotlib-cpp

告诉CMake库的位置，在CMakeLists.txt的project定义之前加：
set(CMAKE_TOOLCHAIN_FILE "[vcpkg安装的父目录]/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")