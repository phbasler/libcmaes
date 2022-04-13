Python3_add_library (lcmaes MODULE lcmaes.cc)

target_link_libraries (lcmaes PRIVATE cmaes Python3::Module Python3::NumPy Boost::python)

if (APPLE)
  set_target_properties (lcmaes PROPERTIES LINK_FLAGS
                                           "-undefined dynamic_lookup")
endif ()

install (TARGETS lcmaes DESTINATION ${PYTHON_SITE_PACKAGES})

set(PathSep ":")
if(WIN32)
  set(PathSep ";")
endif()

set (PYINSTALLCHECK_ENVIRONMENT
  "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}${PathSep}${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}${PathSep}$ENV{PYTHONPATH}"
  )

#if(CMAKE_BUILD_TYPE STREQUAL "")
#set (PYINSTALLCHECK_ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}")
#else()
#set (PYINSTALLCHECK_ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}")
#endif()
message(STATUS "Setting PYTHON to ${PYINSTALLCHECK_ENVIRONMENT}")

if (LIBCMAES_BUILD_TESTS)
  macro (cmaes_add_pytest name)
    add_test (NAME ${name} COMMAND ${Python3_EXECUTABLE}
                                   ${CMAKE_CURRENT_SOURCE_DIR}/${name}.py)
    set_tests_properties (${name} PROPERTIES ENVIRONMENT
                                             "${PYINSTALLCHECK_ENVIRONMENT}")
  endmacro ()

  cmaes_add_pytest (ptest)
  cmaes_add_pytest (ptest_bounds)
  cmaes_add_pytest (ptests_ls)
endif ()
