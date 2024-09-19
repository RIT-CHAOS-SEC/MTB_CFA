projectDir=../../prv/TRACES/
LIST_FILE=$projectDir"NonSecure/Debug/TRACES_NonSecure.list"
TARGET_FILE=$projectDir"Secure/Core/Inc/cfa_engine.h"

OBJDUMP_CMD=arm-none-eabi-objdump

### Secure world
$OBJDUMP_CMD -dz $projectDir/Secure/Debug/TRACES_Secure.elf > objects/Secure.asm.tmp