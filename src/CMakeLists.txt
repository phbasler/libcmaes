
set (LIBCMAES_SOURCES
acovarianceupdate.cc
cmaparameters.cc
cmastopcriteria.cc
covarianceupdate.cc
esostrategy.cc
pwq_bound_strategy.cc
vdcmaupdate.cc
bipopcmastrategy.cc
cmasolutions.cc
cmastrategy.cc
errstats.cc
ipopcmastrategy.cc
surrogatestrategy.cc)

set(header_path "${CMAKE_SOURCE_DIR}/include/libcmaes")
set (LIBCMAES_HEADERS
  ${header_path}/cmaes.h
  ${header_path}/opti_err.h
  ${header_path}/eo_matrix.h
  ${header_path}/cmastrategy.h
  ${header_path}/esoptimizer.h
  ${header_path}/esostrategy.h
  ${header_path}/cmasolutions.h
  ${header_path}/parameters.h
  ${header_path}/cmaparameters.h
  ${header_path}/cmastopcriteria.h
  ${header_path}/ipopcmastrategy.h
  ${header_path}/bipopcmastrategy.h
  ${header_path}/covarianceupdate.h
  ${header_path}/acovarianceupdate.h
  ${header_path}/vdcmaupdate.h
  ${header_path}/pwq_bound_strategy.h
  ${header_path}/eigenmvn.h
  ${header_path}/candidate.h
  ${header_path}/genopheno.h
  ${header_path}/noboundstrategy.h
  ${header_path}/scaling.h
  ${header_path}/llogging.h
  ${header_path}/errstats.h
  ${header_path}/pli.h
  ${header_path}/contour.h)

if (ENABLE_SURROG)
  list (APPEND LIBCMAES_SOURCES surrogatestrategy.cc)
  list (APPEND LIBCMAES_HEADERS ${header_path}/surrcmaes.h ${header_path}/surrogatestrategy.h)
endif ()

include_directories (${CMAKE_CURRENT_SOURCE_DIR})
include_directories (${CMAKE_CURRENT_BINARY_DIR})

add_library (cmaes ${LIBCMAES_HEADERS} ${LIBCMAES_SOURCES})
target_include_directories(cmaes PUBLIC ${CMAKE_SOURCE_DIR}/include ${CMAKE_BINARY_DIR}/include)


if(MSVC)
  target_compile_options(cmaes PRIVATE "/bigobj")
endif()


set_target_properties (cmaes PROPERTIES SOVERSION 0)
set_target_properties (cmaes PROPERTIES VERSION 0.0.0)
set_target_properties (cmaes PROPERTIES POSITION_INDEPENDENT_CODE ON)

# cxx feature detection was unsupported with clang compiler
if (CMAKE_VERSION VERSION_GREATER 3.1 AND USE_COMPILE_FEATURES)
  target_compile_features (cmaes PUBLIC cxx_nonstatic_member_init)
endif ()

include (GenerateExportHeader)
generate_export_header (cmaes)

install ( TARGETS cmaes
          EXPORT  LibcmaesLibraryDepends
          RUNTIME DESTINATION ${RELATIVE_INSTALL_BIN_DIR}
          LIBRARY DESTINATION ${RELATIVE_INSTALL_LIB_DIR}
          ARCHIVE DESTINATION ${RELATIVE_INSTALL_LIB_DIR}
        )

install (FILES ${LIBCMAES_HEADERS} ${CMAKE_CURRENT_BINARY_DIR}/cmaes_export.h
         DESTINATION ${RELATIVE_INSTALL_INCLUDE_DIR}/libcmaes)

if (ENABLE_SURROG)
  install (DIRECTORY ${header_path}/surrogates DESTINATION ${RELATIVE_INSTALL_INCLUDE_DIR}/libcmaes)
endif ()
