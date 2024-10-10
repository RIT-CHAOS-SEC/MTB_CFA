
cmake_minimum_required(VERSION 3.15)

set(command "C:/Users/aj4775/.vcpkg/artifacts/2139c4c6/tools.kitware.cmake/3.28.4/bin/cmake.exe;-G;Ninja;-S;P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2;-B;P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/2;-DSOLUTION_ROOT=P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS;-DCMSIS_PACK_ROOT=C:/Users/aj4775/AppData/Local/arm/packs;-DCMSIS_COMPILER_ROOT=C:/Users/aj4775/.vcpkg/artifacts/2139c4c6/tools.open.cmsis.pack.cmsis.toolbox/2.6.0/etc")
set(log_merged "")
set(log_output_on_failure "ON")
set(stdout_log "P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp/IOTKit_CM33_ns+V2MMPS2-configure-out.log")
set(stderr_log "P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp/IOTKit_CM33_ns+V2MMPS2-configure-err.log")
execute_process(
  COMMAND ${command}
  RESULT_VARIABLE result
  OUTPUT_FILE "${stdout_log}"
  ERROR_FILE "${stderr_log}"
)
macro(read_up_to_max_size log_file output_var)
  file(SIZE ${log_file} determined_size)
  set(max_size 10240)
  if (determined_size GREATER max_size)
    math(EXPR seek_position "${determined_size} - ${max_size}")
    file(READ ${log_file} ${output_var} OFFSET ${seek_position})
    set(${output_var} "...skipping to end...\n${${output_var}}")
  else()
    file(READ ${log_file} ${output_var})
  endif()
endmacro()
if(result)
  set(msg "Command failed: ${result}\n")
  foreach(arg IN LISTS command)
    set(msg "${msg} '${arg}'")
  endforeach()
  if (${log_merged})
    set(msg "${msg}\nSee also\n  ${stderr_log}")
  else()
    set(msg "${msg}\nSee also\n  P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp/IOTKit_CM33_ns+V2MMPS2-configure-*.log")
  endif()
  if (${log_output_on_failure})
    message(SEND_ERROR "${msg}")
    if (${log_merged})
      read_up_to_max_size("${stderr_log}" error_log_contents)
      message(STATUS "Log output is:\n${error_log_contents}")
    else()
      read_up_to_max_size("${stdout_log}" out_log_contents)
      read_up_to_max_size("${stderr_log}" err_log_contents)
      message(STATUS "stdout output is:\n${out_log_contents}")
      message(STATUS "stderr output is:\n${err_log_contents}")
    endif()
    message(FATAL_ERROR "Stopping after outputting logs.")
  else()
    message(FATAL_ERROR "${msg}")
  endif()
else()
  if(NOT "Ninja" MATCHES "Ninja")
    set(msg "IOTKit_CM33_ns+V2MMPS2 configure command succeeded.  See also P:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp/IOTKit_CM33_ns+V2MMPS2-configure-*.log")
    message(STATUS "${msg}")
  endif()
endif()