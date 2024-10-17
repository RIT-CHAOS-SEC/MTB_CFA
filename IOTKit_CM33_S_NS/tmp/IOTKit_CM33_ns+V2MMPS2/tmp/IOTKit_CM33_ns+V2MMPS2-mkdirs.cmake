# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/2"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/tmp"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src"
  "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "D:/Workspace/Git/MTB_CFA/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_ns+V2MMPS2/src/IOTKit_CM33_ns+V2MMPS2-stamp${cfgdir}") # cfgdir has leading slash
endif()
