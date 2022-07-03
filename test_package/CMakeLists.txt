cmake_minimum_required(VERSION 3.1)
project(PackageTest CXX)

list (APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})

include(../cmake/conan.cmake)
conan_cmake_configure(REQUIRES libcmaes/0.10.1-conanReci.d1db8118
                    GENERATORS cmake_find_package
                    )

conan_cmake_autodetect(settings)

conan_cmake_install(PATH_OR_REFERENCE .
  BUILD missing
  SETTINGS ${settings})


find_package(libcmaes 0.10.1 REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example libcmaes::cmaes)

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
