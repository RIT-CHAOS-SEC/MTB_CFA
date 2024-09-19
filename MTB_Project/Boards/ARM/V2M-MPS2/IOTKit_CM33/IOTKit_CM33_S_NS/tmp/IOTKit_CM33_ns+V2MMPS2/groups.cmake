# groups.cmake

# group Source Group 1
add_library(Group_Source_Group_1 OBJECT
  "${SOLUTION_ROOT}/IOTKit_CM33_ns/main_ns.c"
)
target_include_directories(Group_Source_Group_1 PUBLIC
  $<TARGET_PROPERTY:${CONTEXT},INTERFACE_INCLUDE_DIRECTORIES>
)
target_compile_definitions(Group_Source_Group_1 PUBLIC
  $<TARGET_PROPERTY:${CONTEXT},INTERFACE_COMPILE_DEFINITIONS>
)
target_compile_options(Group_Source_Group_1 PUBLIC
  $<TARGET_PROPERTY:${CONTEXT},INTERFACE_COMPILE_OPTIONS>
)
target_link_libraries(Group_Source_Group_1 PUBLIC
  ${CONTEXT}_ABSTRACTIONS
)

# group CMSE Library
add_library(Group_CMSE_Library INTERFACE)
target_include_directories(Group_CMSE_Library INTERFACE
  $<TARGET_PROPERTY:${CONTEXT},INTERFACE_INCLUDE_DIRECTORIES>
  ${SOLUTION_ROOT}/IOTKit_CM33_s
)
target_compile_definitions(Group_CMSE_Library INTERFACE
  $<TARGET_PROPERTY:${CONTEXT},INTERFACE_COMPILE_DEFINITIONS>
)
target_link_libraries(Group_CMSE_Library INTERFACE
  ${SOLUTION_ROOT}/out/IOTKit_CM33_s/V2MMPS2/IOTKit_CM33_s_CMSE_Lib.o
)
