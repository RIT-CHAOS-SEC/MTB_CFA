
path="../IOTKit_CM33_S_NS/IOTKit_CM33_ns/Objects/"
echo ${path}
input_elf=${path}"IOTKit_CM33_ns.axf"
echo ${input_elf}
input_file=${path}"IOTKit_CM33_ns.list"
echo ${input_file}
OBJDUMP=arm-none-eabi-objdump.exe
arch_type="armv8-m33"


grep "word" ${input_file} > .words.tmp
	awk {'print $1, $2'} .words.tmp > .words.tmp2
	sed 's/:/,/g' .words.tmp2 > ./objs/.words


echo "arm-none-eabi-objdump -d" ${input_elf} ">" ${input_file}
arm-none-eabi-objdump -d ${input_elf} > ${input_file}

cp ${input_elf} instrumented.axf

# exit
# rm patched.elf
# rm patched.lst


echo python generate_cfg.py --asmfile ${input_file} --arch ${arch_type} --cfgfile ./objs/cfg.bin
python3 generate_cfg.py --asmfile ${input_file} --arch ${arch_type} --cfgfile ./objs/cfg.bin
echo "Done"

cp instrumented.axf ${path}instrumented.axf

# echo "Running SABRE..."
# python3 sabre.py --cfgfile ./objs/cfg.bin --cflog ${cflog_file} --funcname ${funcname}
# echo "Done"