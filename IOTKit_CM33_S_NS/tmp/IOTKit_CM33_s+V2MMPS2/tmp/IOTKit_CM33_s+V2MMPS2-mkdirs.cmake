# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/1"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/tmp"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/src/IOTKit_CM33_s+V2MMPS2-stamp"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/src"
  "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/src/IOTKit_CM33_s+V2MMPS2-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/src/IOTKit_CM33_s+V2MMPS2-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/nneto/Desktop/MTBTest/Boards/ARM/V2M-MPS2/IOTKit_CM33/IOTKit_CM33_S_NS/tmp/IOTKit_CM33_s+V2MMPS2/src/IOTKit_CM33_s+V2MMPS2-stamp${cfgdir}") # cfgdir has leading slash
endif()
