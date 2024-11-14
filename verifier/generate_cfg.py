from structures import *
from utils import *
from parse_asm import *
import time
import argparse
from patch_ARM import *
import os
import platform
from shutil import which

def arg_parser():
    '''
    Parse the arguments of the program
    Return:
        object containing the arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--asmfile', metavar='N', type=str, required=True,
                        help='Path to the .s asm files generated by objdump')
    parser.add_argument('--cfgfile', metavar='N', type=str, default='cfg.pickle',
                        help='Output file to store serialized CFG. Default is cfg.pickle')
    parser.add_argument('--arch', choices=SUPPORTED_ARCHITECTURES,help='Processor architecture.',
                        default='elf32-msp430')
    
    args = parser.parse_args()
    return args

def process_patch(pg, cfg, patch):
    ## two pass to update instructions of the patch now
    ## First iteration to update the instruction addresses
    patch.bytes = b''.join(patch.bin)
    if patch.instr[0].addr == None:
        pg.mode = 1
        for i in range(0, len(patch.instr)):
            instr = patch.instr[i]
            # print(f"Processing {instr.reconstruct()}")
            patch = add_instruction_ARM(instr, cfg, patch, pg, (None, i))

    ## set addresses of each instruction and correct the offests
    patch.type = 1
    pg.mode = 2
    for i in range(0, len(patch.instr)):
        instr = patch.instr[i]
        patch = add_instruction_ARM(instr, cfg, patch, pg, (None, i))
    patch.instr = sorted(patch.instr, key=lambda x: int(x.addr, 16))
    
    patch.bytes = b''.join(patch.bin)
    pg.patches[patch.addr] = patch
    pg.total_patches += 1
    pg.mode = 0
    patch.type = 0

    return pg

def reconstruct_nscs(cfg, asm_funcs):
    main_addr = cfg.label_addr_map['main']
    # print(f"main: {main_addr}")
    main_func = asm_funcs[main_addr]
    # print(f"main_func : \n{main_func}\n")
    nsc_to_veneers = {}
    for i in range(0, len(main_func.instr_list)):
        instr = main_func.instr_list[i]
        if 'ip' in instr.arg:
            # print(f"{instr.addr} {instr.reconstruct()}")
            if 'movw' in instr.instr: # get the lower half
                veneer_addr = instr.addr
                imm = instr.arg.split(", #")[1]
                lower = int(imm.split('@')[0])
            elif 'movt' in instr.instr: # get the upper half
                imm = instr.arg.split(", #")[1]
                upper = 0 | (int(imm.split('@')[0]) << 16)
            else: #bx ip
                # print(f"\t veneer_addr : {veneer_addr}")
                # print(f"\t lower : {hex(lower)}")
                # print(f"\t upper : {hex(upper)}")
                # print(f"\t ip_val : {hex(ip_val)}")
                sg_addr = (upper | lower) - 1
                nsc_to_veneers[hex(sg_addr)] = veneer_addr

    for sg in nsc_to_veneers:
        print(f"{sg} : {nsc_to_veneers[sg]}")
    # a = input()
    return nsc_to_veneers

def instrument(cfg, asm_funcs):
    '''
    Function for instrumenting a binary from the diassembled instructions
    '''
    print("LOOP DESTS")
    loop_dests = []
    loop_dest_mapping = {}
    loop_branches = []
    for ln in cfg.loop_nodes:
        dest = '0x'+cfg.nodes[ln].instr_addrs[-1].arg.split(' ')[0]
        loop_dests.append(dest)
        loop_dest_mapping[dest] = ln
        loop_branches.append(cfg.nodes[ln].instr_addrs[-1].addr)
    for ln in cfg.inner_loop_nodes:
        loop_branches.append(cfg.nodes[ln].instr_addrs[-1].addr)
    print(f"Loop branches : {loop_branches}")
    # a = input()

    sglistFile = open("./sg.lst", "r")
    sglist = [x.replace('\n', '') for x in sglistFile.readlines()]
    sglistFile.close()
    sg_mapping = {}
    for elt in sglist:
        addr, func = elt.split(' <')
        func = func.replace(">:", "")
        addr = '0x'+addr
        sg_mapping[func] = addr
    print(sglist)
    for func, addr in sg_mapping.items():
        print(f"{func} --> {addr}")
    # a = input()

    pg = PatchGenerator(cfg.arch.patch_base)

    tr_pg = PatchGenerator(cfg.arch.trampoline_region)

    MTBDR_MIN = 0x300000    
    MTBDR_MAX = 0x360000    
    # func_labels = ['application']#, 'NonSecure_LED_Off']

    #### first addition: add a veneer for secure_log_loop_cond into the tr region
    log_loop_cond_sg_addr = sg_mapping['SECURE_log_loop_cond']
    lower = log_loop_cond_sg_addr[:6]
    upper = "0x"+log_loop_cond_sg_addr[6:]
    print(f"log_loop_cond_sg_addr : {log_loop_cond_sg_addr}")
    print(f"lower : {lower}")
    print(f"upper : {upper}")
    tr_patch = Patch(f'veneer-tr')
    asm = AssemblyInstruction(addr=None, instr='movw', arg=f'ip, #{int(upper,16)+1}')
    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
    asm = AssemblyInstruction(addr=None, instr='movt', arg=f'ip, #{int(lower,16)}')
    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
    asm = AssemblyInstruction(addr=None, instr='bx', arg=f'ip')
    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
    tr_pg = process_patch(tr_pg, cfg, tr_patch)
    nsc_addr = tr_patch.instr[0].addr
    print(f"Nsc_addr : {nsc_addr}")
    # a = input()

    # func = asm_funcs[cfg.label_addr_map['NonSecure_LED_Off']]
    for func_addr in asm_funcs.keys():
        skip = True
        for instr in asm_funcs[func_addr].instr_list:
            if instr.instr in cfg.arch.indr_calls or instr.instr in cfg.arch.conditional_br_instrs:
                skip = False

        if skip:
            continue

        if 'rand_beebs' in cfg.label_addr_map.keys():
            if func_addr == cfg.label_addr_map['rand_beebs']:
                continue

        if func_addr == cfg.label_addr_map['application_entry']:
            print("AAAAAA !!!!!!")
            continue

        print(func_addr)
        if MTBDR_MIN <= int(func_addr,16) and MTBDR_MAX > int(func_addr,16):
            print(f"doing {func_addr}")
            func = asm_funcs[func_addr]    
            i = 0
            while i < len(func.instr_list):
                instr = func.instr_list[i]

                if instr.instr == 'push' and 'lr' not in instr.arg:
                    mtbdr_patch = Patch(instr.addr)
                    new_arg = instr.arg.replace("}", ", lr}")
                    asm = AssemblyInstruction(addr=instr.addr, instr=instr.instr, arg=new_arg)
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    sp_offset_instr = func.instr_list[i+1]
                    arg_front = sp_offset_instr.arg.split("#")[0]+'#'
                    sp_offset_instr.arg = sp_offset_instr.arg.split('@')[0]
                    new_sp_offset = str(int(sp_offset_instr.arg.split("#")[1])-4)
                    asm = AssemblyInstruction(addr=sp_offset_instr.addr, instr=sp_offset_instr.instr, arg=arg_front+new_sp_offset)
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)

                if instr.instr == 'bx' and 'lr' in instr.arg:
                    prev_instr = func.instr_list[i-1]
                    sp_change_instr = func.instr_list[i-2]
                    sp_offset_instr = func.instr_list[i-3]
                    mtbdr_patch = Patch(prev_instr.addr)
                    arg_front = sp_offset_instr.arg.split("#")[0]+'#'
                    sp_offset_instr.arg = sp_offset_instr.arg.split('@')[0]
                    print(sp_offset_instr.arg)
                    print(instr.addr)
                    new_sp_offset = str(int(sp_offset_instr.arg.split("#")[1])-4)

                    asm = AssemblyInstruction(addr=sp_offset_instr.addr, instr=sp_offset_instr.instr, arg=arg_front+new_sp_offset)
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)

                    asm = AssemblyInstruction(addr=sp_change_instr.addr, instr=sp_change_instr.instr, arg=sp_change_instr.arg)
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)

                    asm = AssemblyInstruction(addr=prev_instr.addr, instr='pop', arg='{r7, pc}')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    asm = AssemblyInstruction(addr=hex(int(prev_instr.addr,16)+2), instr='nop', arg='')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    asm = AssemblyInstruction(addr=instr.addr, instr='nop', arg='')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)

                if instr.instr == 'pop' and 'pc' not in instr.arg:
                    mtbdr_patch = Patch(instr.addr)
                    new_arg = instr.arg.replace("}", ", pc}")
                    asm = AssemblyInstruction(addr=instr.addr, instr=instr.instr, arg=new_arg)
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)

                alt_ret = ('pop' in instr.instr and 'pc' in instr.arg) or ('ldr' == instr.instr and 'pc' in instr.arg.split(', ')[0])

                print(f"{instr.addr} {instr.reconstruct()}")
                #'''
                if instr.addr in loop_dests:
                    do_nothing = 0
                    
                    print(f"FOUND ONE IN HTE LOOP NODES : {instr.addr}")
                    # a = input()

                    prev_instr = func.instr_list[i-1]
                    if prev_instr.instr in cfg.arch.all_br_insts:
                        prev_instr = func.instr_list[i-2]
                        prev_prev_instr = func.instr_list[i-3]

                        # we are replacing two instructions with 4 bytes.
                        ### so if the two add up to 6, we need a nop
                        if int(prev_instr.addr,16)-int(prev_prev_instr.addr,16) == 4:
                            needNop = True
                        else:
                            needNop = False
                    
                    ### need a spot in the TR that adds prev_instr's and b's to the NSC veneer (also in the TR)
                    tr_patch = Patch(f'{instr.addr}-tr')
                    asm = AssemblyInstruction(addr=None, instr=prev_prev_instr.instr, arg=f'{prev_prev_instr.arg}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    asm = AssemblyInstruction(addr=None, instr=prev_instr.instr, arg=f'{prev_instr.arg}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    ### also need to move the condition to r10 before calling the nsc
                    ## first find the loop node
                    loop_node_addr = loop_dest_mapping[instr.addr] # instr.addr holds the loop_dest
                    ## by convention, the cmp will be second to last
                    loop_cond_val = cfg.nodes[loop_node_addr].instr_addrs[-2].arg.split(', ')[0]
                    ## move the loop_cond_val to r10
                    asm = AssemblyInstruction(addr=None, instr='mov', arg=f'r10, {loop_cond_val}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    ## finally b to the nsc
                    asm = AssemblyInstruction(addr=None, instr='b', arg=f'{nsc_addr[2:]}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    tr_pg = process_patch(tr_pg, cfg, tr_patch)

                    #### replace the prev instr in MTBDR with a bl to the TR
                    mtbdr_patch = Patch(f'{tr_patch.addr}-tr')
                    tr_addr = tr_patch.instr[0].addr[2:]
                    asm = AssemblyInstruction(addr=prev_prev_instr.addr, instr='bl', arg=f'{tr_addr}')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    if needNop:
                        asm = AssemblyInstruction(addr=hex(int(prev_prev_instr.addr,16)+4), instr='nop', arg=f'')
                        mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)
                #'''
                if instr.instr in cfg.arch.conditional_br_instrs and instr.addr not in loop_branches:

                    instr.arg = instr.arg.split(' ')[0]
                    prev_instr = func.instr_list[i-1]
                    
                    prev_instr = func.instr_list[i-1]
                    if '@' in instr.arg:
                        instr.arg = instr.arg.split('@')[0]
                    if '@' in prev_instr.arg:
                        prev_instr.arg = prev_instr.arg.split('@')[0]

                    '''
                    if int(instr.arg, 16) < int(instr.addr,16):
                    print("ENTERED LS THAN CASE") # branch taken is in the MTBAR
                    a = input()
                    '''
                    ## add dir branch to the cb dest in MTBAR
                    mtbar_patch = Patch(instr.addr)
                    for k in range(0, 7):
                        asm = AssemblyInstruction(addr=None, instr='nop', arg=f'')
                        mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                    asm = AssemblyInstruction(addr=None, instr='b.w', arg=f'{instr.arg}')
                    mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                    pg = process_patch(pg, cfg, mtbar_patch)

                    ## in TR region add cmp, cond_br to MTBAR, and b back to MTBDR
                    tr_patch = Patch(f'{instr.addr}-tr')
                    asm = AssemblyInstruction(addr=None, instr=prev_instr.instr, arg=f'{prev_instr.arg}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    asm = AssemblyInstruction(addr=None, instr=instr.instr, arg=f'{hex(int(mtbar_patch.instr[0].addr, 16)-4)}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)

                    next_instr = func.instr_list[i+1]
                    print(next_instr.reconstruct())
                    if next_instr.instr in cfg.arch.unconditional_br_instrs:
                        asm = AssemblyInstruction(addr=None, instr='b.w', arg=f"{next_instr.arg}")
                    else:
                        asm = AssemblyInstruction(addr=None, instr='b.n', arg=f'{hex(int(prev_instr.addr, 16)+4)}')
                    print(asm.reconstruct())
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    tr_pg = process_patch(tr_pg, cfg, tr_patch)
                    
                    ## from MTBDR we need to b into the TR region
                    mtbdr_patch = Patch(f'{tr_patch.addr}-tr')
                    tr_addr = tr_patch.instr[0].addr[2:]
                    asm = AssemblyInstruction(addr=prev_instr.addr, instr='b.w', arg=f'{tr_addr}')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)

                    '''
                    else:
                    print(instr.addr)
                    print("ENTERED GT THAN CASE") #branch taken is not in the MTBAR
                    a = input()
                    ## add dir branch to the next_instr in MTBAR
                    mtbar_patch = Patch(instr.addr)
                    for k in range(0, 7):
                        asm = AssemblyInstruction(addr=None, instr='nop', arg=f'')
                        mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)

                    next_instr = func.instr_list[i+1]
                    print(f"next instr: {next_instr.addr} {next_instr.reconstruct()}")
                    a = input()
                    if next_instr.instr in cfg.arch.unconditional_br_instrs:
                        asm = AssemblyInstruction(addr=None, instr='b.w', arg=f"{next_instr.arg}")
                    else:
                        asm = AssemblyInstruction(addr=None, instr='b.n', arg=f'{hex(int(next_instr.addr, 16)+4)}')
                    mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                    pg = process_patch(pg, cfg, mtbar_patch)
                    

                    ## in TR region add cmp, cond_br to MTBDR, and b to MTBAR
                    tr_patch = Patch(f'{instr.addr}-tr')
                    asm = AssemblyInstruction(addr=None, instr=prev_instr.instr, arg=f'{prev_instr.arg}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    asm = AssemblyInstruction(addr=None, instr=instr.instr, arg=f"{hex(int(instr.arg, 16)-4)}")
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    asm = AssemblyInstruction(addr=None, instr='b.w', arg=f"{mtbar_patch.instr[0].addr}")
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                    tr_pg = process_patch(tr_pg, cfg, tr_patch)

                    ## from MTBDR we need to b into the TR region
                    mtbdr_patch = Patch(f'{tr_patch.addr}-tr')
                    tr_addr = tr_patch.instr[0].addr[2:]
                    asm = AssemblyInstruction(addr=prev_instr.addr, instr='b.w', arg=f'{tr_addr}')
                    mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                    pg = process_patch(pg, cfg, mtbdr_patch)
                    '''

                elif instr.instr in cfg.arch.indr_calls: #indr_calls
                    print(f"Call at {instr.addr}")
                    ### add a trampoline to the call's dest
                    mtbar_patch = Patch(instr.addr)
                    asm = AssemblyInstruction(addr=None, instr='b.n', arg=f'{instr.arg}')
                    mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                    pg = process_patch(pg, cfg, mtbar_patch)
                    
                    ## add trampoline from og addr into MTBAR
                    tr_patch = Patch(f'{instr.addr}-tr')
                    asm = AssemblyInstruction(addr=instr.addr, instr=instr.instr, arg=f'{mtbar_patch.instr[0].addr[2:]}')
                    tr_patch = add_instruction_ARM(asm, cfg, tr_patch, pg)
                    pg = process_patch(pg, cfg, tr_patch)

                #''''
                elif alt_ret:
                    print(f"Return at {instr.addr}")
                    ## return is last instruction, and we need two spaces for the b.w
                    ## therefore, we take the previous instruction with us too
                    prev_instr = func.instr_list[i-1]
                    if '@' in instr.arg:
                        instr.arg = instr.arg.split('@')[0]
                    if '@' in prev_instr.arg:
                        prev_instr.arg = prev_instr.arg.split('@')[0]

                    #'''
                    print(f"checking {prev_instr.instr} in {cfg.arch.call_instrs}")
                    # a = input()
                    if prev_instr.instr in cfg.arch.call_instrs:
                        ## in this case: instr      =  pop/ldr to pc
                        ##               prev_instr =  a bl -- all other branch instructions are handled naturally


                        ## MTBAR implements the return instruction
                        mtbar_patch = Patch(instr.addr)
                        asm = AssemblyInstruction(addr=None, instr=instr.instr, arg=f'{instr.arg}')
                        mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                        pg = process_patch(pg, cfg, mtbar_patch)
                        print(" got here !")
                        ## trampoline region should have the prev instrucition, then a b.w. to the MTBAR
                        tr_patch = Patch(f'{prev_instr.addr}-tr')
                        asm = AssemblyInstruction(addr=None, instr=prev_instr.instr, arg=f"{prev_instr.arg.split(' ')[0]}")
                        tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                        asm = AssemblyInstruction(addr=None, instr='b.w', arg=f'{mtbar_patch.instr[0].addr[2:]}')
                        tr_patch = add_instruction_ARM(asm, cfg, tr_patch, tr_pg)
                        tr_pg = process_patch(tr_pg, cfg, tr_patch)
                        print(" got here !!")
                        ## direct branch in MTBDR to the trampoline region
                        mtbdr_patch = Patch(f'{tr_patch.addr}-tr')
                        asm = asm = AssemblyInstruction(addr=prev_instr.addr, instr='b.w', arg=f'{tr_patch.instr[0].addr[2:]}')
                        mtbdr_patch = add_instruction_ARM(asm, cfg, mtbdr_patch, pg)
                        pg = process_patch(pg, cfg, mtbdr_patch)
                        print(" got here !!!")
                    else:
                        #'''
                        print(instr.arg)
                        ### move ret instr and prev into the MTBAR
                        mtbar_patch = Patch(prev_instr.addr)
                        for k in range(0, 7):
                            asm = AssemblyInstruction(addr=None, instr='nop', arg=f'')
                            mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                        asm = AssemblyInstruction(addr=None, instr=prev_instr.instr, arg=f'{prev_instr.arg}')
                        mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                        asm = AssemblyInstruction(addr=None, instr=instr.instr, arg=f'{instr.arg}')
                        mtbar_patch = add_instruction_ARM(asm, cfg, mtbar_patch, pg)
                        pg = process_patch(pg, cfg, mtbar_patch)

                        # ### trampoline to the ret
                        tr_patch = Patch(f'{prev_instr.addr}-tr')
                        asm = AssemblyInstruction(addr=prev_instr.addr, instr='b.w', arg=f'{mtbar_patch.instr[0].addr[2:]}')
                        tr_patch = add_instruction_ARM(asm, cfg, tr_patch, pg)
                        pg = process_patch(pg, cfg, tr_patch)
                #'''
                i += 1

    # print("---------------")
    # for addr, patch in pg.patches.items():
    #     print(f"Patch at {addr}")
    #     for instr in patch.instr:
    #         print(instr)
    #     print('\n')

    ## iterate over the patches and add the 
    elf_file_path = 'instrumented.axf'
    count=0
    print("---- Updating ELF ----")
    for addr, patch in pg.patches.items():
        print(f"Updating ELF with patch {addr}...")
        for i in range(0, len(patch.instr)):
            instr_addr = int(patch.instr[i].addr, 16)
            print(f"Updating {patch.instr[i].addr} to {patch.bin[i]}")
            update_instruction(cfg.arch, elf_file_path, instr_addr, patch.bin[i])
        count += 1
        # break
    # a = input()
    print()
    for addr, patch in tr_pg.patches.items():
        print(f"Updating ELF with patch {addr}...")
        for i in range(0, len(patch.instr)):
            instr_addr = int(patch.instr[i].addr, 16)
            print(f"Updating {patch.instr[i].addr} to {patch.bin[i]}")
            update_instruction(cfg.arch, elf_file_path, instr_addr, patch.bin[i])
        count += 1
        # break
    # a = input()
    print()
    
    os_type = platform.system()

    # check if command arm-none-eabi-objdump exist in the system
    def check_command_exists(command):
        return which(command) is not None

    bash_cmd = "arm-none-eabi-objdump -d ./instrumented.axf > ./instrumented.lst"
    if not check_command_exists("arm-none-eabi-objdump"):
        bash_cmd = "arm-none-eabi-objdump.exe -d ./instrumented.axf > ./instrumented.lst"
        #raise EnvironmentError("arm-none-eabi-objdump command not found in the system PATH")


    # if os_type == "Linux":
    #     bash_cmd = "arm-none-eabi-objdump -d ./instrumented.axf > ./instrumented.lst"
    # else:
    #     bash_cmd = "arm-none-eabi-objdump.exe -d ./instrumented.axf > ./instrumented.lst"
    
    os.system(bash_cmd)

def main():
    start = time.perf_counter()
    args = arg_parser()

    # Set arch if provided
    arch = set_arch(args.arch)

    # Parse asm file to python object
    lines = read_file(args.asmfile, arch.type)

    asm_func_file = args.cfgfile.replace("cfg", "asm_func")

    # Create the CFG from the asm file
    cfg, asm_funcs = create_cfg(arch, lines)

    # Serialize cfg to output file
    dump(cfg,args.cfgfile)

    dump(asm_funcs,asm_func_file)
    stop = time.perf_counter()
    timingFile = open('./logs/timing.log', 'w')
    print(f"Build CFG: {1000*(stop-start)} ms", file=timingFile)
    timingFile.close()

    debugFile = open("./logs/debug.log", "w")
    print("Nodes", file=debugFile)
    print("-------------------", file=debugFile)
    
    for node in cfg.nodes.keys():
        cfg.nodes[node].printNode(debugFile)
        print("", file=debugFile)
    print("-------------------", file=debugFile)
    print(f"Total Indr Calls: {len(cfg.indr_calls)}")
    
    if len(cfg.indr_calls) > 0:
        print("Indirect Calls:", file=debugFile)
        for addr in cfg.indr_calls:
            cfg.nodes[addr].printNode(debugFile)
        print("-------------------", file=debugFile)
        print("", file=debugFile)

    print(f"Total Indr Jumps: {len(cfg.indr_jumps)}")
    if len(cfg.indr_jumps) > 0:
        print("Indirect Jumps:", file=debugFile)
        for addr in cfg.indr_jumps:
            cfg.nodes[addr].printNode(debugFile)
        print("-------------------", file=debugFile)
        print("", file=debugFile)
    
    
    if len(cfg.func_nodes.keys()) > 0:
        print(f"Func nodes: {len(cfg.func_nodes.keys())}")
        for key in cfg.func_nodes.keys():
            print(f"{key}: {cfg.func_nodes[addr]}")
        print("-------------------", file=debugFile)
        print("", file=debugFile)

    print(f"Label addr map")
    for label in cfg.label_addr_map:
        print(f"{label} : {cfg.label_addr_map[label]}", file=debugFile)
    debugFile.close()

    print("Reconstructing NSCs")
    cfg.nsc_to_veneers = reconstruct_nscs(cfg, asm_funcs)

    print("Running instrument")
    instrument(cfg, asm_funcs)

if __name__ == "__main__":
    main()