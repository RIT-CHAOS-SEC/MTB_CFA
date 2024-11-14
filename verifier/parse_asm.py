from structures import *
from utils import *
from collections import deque
from os import system, name
import multiprocessing

def parse_asm_functions(arch,assembly_lines):
    '''
        Description:
            Read a file generated by the command: msp430-objdump -d <executable_file_name> and fill the AssemblyFunction struct
        Input:
            assembly_lines: lines of the <executable_file> generated by .readlines() 
        Output: 
            AssemblyFunction struct
    '''

    # All the information will be here
    assembly_functions = {}
    assembly_functions_name_mapping = {}
    instructions = []

    # Filter the 'Disassembly of section .text:' region
    ## Filter the beginning

    beg_id = 0
    print(f"total lines: {len(assembly_lines)}")
    print(f"assembly_lines[beg_id] = {assembly_lines[beg_id]}")
    while(assembly_lines[beg_id].find(TEXT_PATTERN[0])<0) :
        beg_id = beg_id+1

    ## Filter the end     
    end_id = beg_id+1
    # while(assembly_lines[end_id].find(TEXT_PATTERN[1])<0 and end_id < len(assembly_lines)-1):
    while(end_id < len(assembly_lines)-1):
        end_id = end_id+1

    if end_id < len(assembly_lines)-1:
        assembly_lines = assembly_lines[beg_id:end_id]
    else:
        assembly_lines = assembly_lines[beg_id:]

    # Parse each line

    for line in assembly_lines:
        s = line.split(' ')
        # print(line)
        # a = input()
        
        # Attempt to detect the architecture type if not provided
        if 'file format' in line:
            if arch is None:
                arch = set_arch(s[-1])
            
        # Extract assembly labels and addresses 
        elif '<' in line and '>' in line and len(s) == 2: 
            # if arch.type == 'elf32-msp430' or (arch.type == 'armv8-m33' and arch.instrumentation_handle not in line):
            label = s[1][1:-2]
            addr = '0x'+ s[0].lstrip('0')
            assembly_functions_name_mapping[label] = addr
        # Else parse 
        elif line != '' and ':' in line: 
            
            # Separate Comments from command
            c = line.split(';')
            if len(c)>1:
                comment = c[1]
            else:
                comment = ''

            c = c[0].split('\t')
            # Remove if there is no instruction in the line
            # print(f"({len(c)}) adding {c}")
            if len(c) <= 2:
                continue
            
            # Find memory address
            addr = '0x' + c[0].replace(' ','').replace(':','')
            
            # Find instruction
            if len(c) > 2:
                instr = c[2]
            else:
                instr = ''

            # Find instr argument
            arg = ''
            for arg_s in c[3:]:
                arg+=arg_s

            # Add information to the struct and add to instr list
            asm = AssemblyInstruction(addr,instr.replace(' ',''),arg.replace('\t',''),comment)
            instructions.append(asm)
            

    done = False

    # a = input()
    # Parse instructions into functions
    while not done: 
        for i in range(len(instructions)): 
            '''
            # direct return instruction
            detect_ret = (instructions[i].instr in arch.return_instrs)
            inf_loop = (instructions[i].instr in arch.unconditional_br_instrs) and (instructions[i].addr[2:] in instructions[i].arg)
            
            if arch.type == 'elf32-msp430':
                ## special case for msp430 since main does not have a ret instruction
                detect_ret = detect_ret or (instructions[i].addr == assembly_functions_name_mapping['__isr_0'])
            
            # detect default arm funcs ending in while loop (such as Error Handler)
            elif arch.type == 'armv8-m33' and inf_loop:
                print(f"{instructions[i].addr} in {instructions[i].arg}")
                detect_ret = detect_ret or inf_loop
            # detect return via pop to pc (sometimes in ARM)
            detect_ret_via_pop = (instructions[i].instr == "pop" and "pc" in instructions[i].arg)
            secure_ret = (arch.instrumentation_handle in instructions[i].arg) and ('ret' in instructions[i].arg)
            if detect_ret or detect_ret_via_pop or secure_ret: #Scan till ret instr
                f = AssemblyFunction(instructions[0].addr, instructions[i].addr, instructions[:i+1])
                
                assembly_functions[f.start_addr] = f
                #print(instructions)
                instructions = instructions[i+1:] # remove func instrs from list
                break
    
            # Not a return -- Check if this is the last instr of the file
            elif instructions[i] == instructions[-1]:
                done = True
            '''
            if i != 0 and instructions[i].addr in assembly_functions_name_mapping.values():
                # print(f"{instructions[i].addr} in addr_mapping")

                f = AssemblyFunction(instructions[0].addr, instructions[i-1].addr, instructions[:i])
                # print("")
                # print(f"Adding new func: {f.start_addr}, {f.end_addr}")
                # print(f"first instr: {f.instr_list[0].addr}")
                # print(f"last instr: {f.instr_list[-1].addr}")
                # a = input()
                assembly_functions[f.start_addr] = f
                #print(instructions)
                instructions = instructions[i:] # remove func instrs from list
                break

            # Not a return -- Check if this is the last instr of the file
            elif instructions[i] == instructions[-1]:
                done = True
        
        # Add any instrs not in func to extra "func" to be parsed as nodes
        if len(instructions) != 0:
            f = AssemblyFunction(instructions[0].addr, instructions[-1].addr, instructions)
            assembly_functions[f.start_addr] = f
        else:
            done = True

    return arch,assembly_functions,assembly_functions_name_mapping
       
def parse_nodes(arch,assembly_functions,cfg):
    # print(f"br_instrs: {br_instrs}")
    added = True
    for func_addr,func in assembly_functions.items():
        if added:
            # to account for labels that are not "funcs"
            added = False
            # print(f"starting from {func.start_addr}")
            node = CFGNode(func.start_addr,func.end_addr)
        # else:
            # print(f"continuing from {func.start_addr}")

        # iterating over indexes so that we can grab adj instrs as well
        for i in range(len(func.instr_list)):

            #add instruction to node
            node.add_instruction(func.instr_list[i])
            
            #check for br instr, if found create node
            # print(f"Pasring ... {func.instr_list[i].addr}: {func.instr_list[i].instr} {func.instr_list[i].arg}")
            ret_via_pop = (func.instr_list[i].instr == "pop" and "pc" in func.instr_list[i].arg) # check for ret via pop
            instrumented_call = (arch.instrumentation_handle in func.instr_list[i].arg) and  (func.instr_list[i].instr in arch.call_instrs)            
            # secure_ret = (arch.instrumentation_handle in func.instr_list[i].arg) and ('ret' in func.instr_list[i].arg)
            secure_ret = False
            ## other_handlers = (arch.instrumentation_handle in func.instr_list[i].arg) and not ('call' in func.instr_list[i].arg) and not ('ret' in func.instr_list[i].arg)                        
            branch_trampoline = (arch.instrumentation_handle in func.instr_list[i].arg) and ('cond_br' in func.instr_list[i].arg)          

            # print(func.instr_list[i].addr)
            # print(ret_via_pop)
            # print(instrumented_call)
            # print(secure_ret)
            # print(other_handlers)
            # print(" ")
            # print(f"arch.type: {arch.type}")
            if arch.type == 'elf32-msp430':
                if (ret_via_pop or func.instr_list[i].instr in arch.all_br_insts):
                    node.end_addr = func.instr_list[i].addr
                    # print(f"Ending node at {node.end_addr}") 
                    if func.instr_list[i].instr in arch.conditional_br_instrs:
                        node.type = 'cond'
                    elif func.instr_list[i].instr in arch.unconditional_br_instrs:
                        node.type = 'uncond'
                    elif (func.instr_list[i].instr in arch.call_instrs):
                        node.type = 'call'
                    elif func.instr_list[i].instr in arch.return_instrs:
                        node.type = 'ret'
                        func.return_node = node

                    #add node to cfg dict
                    # print(node.type)
                    # a = input()
                    added = True
                    # if node.start_addr == "0xe018":
                    # print(f'{node.start_addr}\t{node.adj_instr}\t{i}\t{len(func.instr_list)}')   
                    cfg.add_node(node,func_addr)
                    # print(f"Adding node '{node.start_addr}'")
                    #add adj instrs to prev nodes
                    if i+1 < len(func.instr_list): # bounds check
                        node.adj_instr = func.instr_list[i+1].addr
                        #create a new node
                        # print(f"Starting node from {node.adj_instr}")  
                        node = CFGNode(node.adj_instr,node.adj_instr) 
                    elif func.instr_list[i].instr in arch.conditional_br_instrs:
                        node.adj_instr = hex(int(node.end_addr, 16)+arch.regular_instr_size)
                    # a = input()

            elif arch.type == 'armv8-m33':
                trampoline_via_dir_jump = (arch.instrumentation_handle in func.instr_list[i].arg) and (func.instr_list[i].instr in arch.unconditional_br_instrs)
                try:
                    prev_write_to_pc = (arch.indr_tgt_reg in func.instr_list[i-1].arg) and (func.instr_list[i].instr in arch.unconditional_br_instrs)
                except IndexError:
                    prev_write_to_pc = False
                indr_jump_via_write = trampoline_via_dir_jump and prev_write_to_pc

                # if trampoline_via_dir_jump:
                #     print(f"trampoline_via_dir_jump is True: {func.instr_list[i]}")
                #     print(f"prev_write_to_pc is {prev_write_to_pc}: {func.instr_list[i-1]}")
                #     print(f"indr_jump_via_write is {indr_jump_via_write}\n")

                if (secure_ret or (ret_via_pop or func.instr_list[i].instr in arch.all_br_insts) or instrumented_call) and not branch_trampoline:
                    node.end_addr = func.instr_list[i].addr
                    if func.instr_list[i].instr in arch.conditional_br_instrs:
                        node.type = 'cond'
                    elif secure_ret or (func.instr_list[i].instr in arch.return_instrs) or ret_via_pop:
                        # if ret_via_pop:
                            # print(f"ret_via_pop at {func.instr_list[i].addr}")
                        node.type = 'ret'
                        func.return_node = node
                    elif (func.instr_list[i].instr in arch.call_instrs):
                        node.type = 'call'
                    elif func.instr_list[i].instr in arch.unconditional_br_instrs or indr_jump_via_write:
                        node.type = 'uncond'
                        if indr_jump_via_write:
                            print(f"Indr_jump via write: \n\t{func.instr_list[i-1]}\n\t{func.instr_list[i]}\n")                
            
                    # #add node to cfg dict
                    # print(node.start_addr)
                    # print(node.type)
                    # a = input()
                    added = True
                    cfg.add_node(node,func_addr)
                    
                    #add adj instrs to prev nodes 
                    if i+1 < len(func.instr_list): # bounds check
                        node.adj_instr = func.instr_list[i+1].addr
                        #create a new node
                        node = CFGNode(node.adj_instr,node.adj_instr)                
        
    return cfg

def update_successors(arch,asm_funcs,cfg):
    succ_in_range = 0
    succ_out_of_range = 0

    nodes_to_add = []
    addrs = list(cfg.nodes.keys())
    for i in range(0, len(addrs)):
    # node_addr,node in cfg.nodes.items()
        node_addr = addrs[i]
        node = cfg.nodes[node_addr]
        if node.type == "cond":
            if node.adj_instr:
                node.add_successor(node.adj_instr)
            if arch.type == 'elf32-msp430':
                succ = clean_comment(arch, node.instr_addrs[-1].comment)
                node.add_successor(succ)

            elif arch.type == "armv8-m33":
                # cbz and cbnz have two args
                if 'cbz' in node.instr_addrs[-1].instr or 'cbnz' in node.instr_addrs[-1].instr:
                    a = "0x"+node.instr_addrs[-1].arg.split(' ')[1]
                else:
                    a = "0x"+node.instr_addrs[-1].arg.split(' ')[0]
                # print("adding successor: "+str(a))
                node.add_successor(a)
        elif node.type == "uncond":
            if arch.type == 'elf32-msp430':
                #first try to parse address from the arg
                a = clean_comment(arch, node.instr_addrs[-1].arg)
                if a:
                    node.add_successor(a)
                else:
                    a = clean_comment(arch, node.instr_addrs[-1].comment)
                    # If none (i.e addr is relative), parse the address from the comment
                    if a:
                        node.add_successor(a)
                    else:
                        # there's no comment because it is an its an indirect jump
                        # print(f"indr_call:\ttype:{node.type}, Node:({node.start_addr}, {node.end_addr}), instruction: {node.instr_addrs[-1].instr} {node.instr_addrs[-1].arg}")
                        cfg.indr_jumps.append(node.start_addr)
                        continue 

            elif arch.type == "armv8-m33":
                if arch.instrumentation_handle in node.instr_addrs[-1].arg and arch.indr_tgt_reg in node.instr_addrs[-2].arg:
                    # print(f"indr_call:\ttype:{node.type}, Node:({node.start_addr}, {node.end_addr}), instruction: {node.instr_addrs[-1].instr} {node.instr_addrs[-1].arg}")
                    cfg.indr_jumps.append(node.start_addr)
                else:
                    # normal dir branch
                    a = "0x"+node.instr_addrs[-1].arg.split(' ')[0]
                    node.add_successor(a)

        elif node.type == "call":
            if arch.type == 'elf32-msp430':
                indr_call = 'r' in node.instr_addrs[-1].arg
                br_dest = clean_comment(arch, node.instr_addrs[-1].arg)
            elif arch.type == "armv8-m33":
                indr_call = False
                # indr_call = arch.instrumentation_handle in node.instr_addrs[-1].arg
                br_dest = "0x"+node.instr_addrs[-1].arg.split(' ')[0]
                # print(f"call in node {node.start_addr}")
                # print(br_dest)

            if indr_call == True:
                # handled later on...c
                # print(f"indr_call={indr_call}, type:{node.type}, Node:({node.start_addr}, {node.end_addr}), instruction: {node.instr_addrs[-1].instr} {node.instr_addrs[-1].arg}")
                cfg.indr_calls.append(node.start_addr)
                continue 
            
            node.add_successor(br_dest)
            
            try:
                ret_node = asm_funcs[br_dest].return_node
                if ret_node is not None:
                    # print(f"Call from {node.end_addr}")
                    # print(f"Return node {ret_node.start_addr} of func {br_dest}")
                    ret_node.add_successor(node.adj_instr)
                    # a = input()
            except KeyError:
                print(f'key error adding return node of func {br_dest}')

        # Add check to make sure all branching destinations are existing nodes
        # If not, create a new node
        for succ_addr in node.successors:
            if succ_addr is not None and succ_addr not in cfg.nodes.keys():
                # print(f"{succ_addr} is not None and {succ_addr} not in cfg.nodes {type(cfg.nodes)}")
                # This should prob be optimized
                
                for n in cfg.nodes.values():
                    # if succ_addr == "0xe15e":
                        # print(f"{n.start_addr} <= {succ_addr} <= {n.end_addr}")
                    new_node = None
                    if succ_addr >= n.start_addr and succ_addr <= n.end_addr:
                        # print(f"s\t creating Node({n.start_addr},{n.end_addr})"
                        new_node = CFGNode(succ_addr,n.end_addr)
                        new_node.type = n.type
                        new_node.successors = n.successors  
                        new_node.adj_instr = n.adj_instr 
                        new_node.instr_addrs = n.instr_addrs
                        # if new_node.start_addr == "0xe018":
                            # print(f'\t new_node {node.adj_instr}')

                        stop = False
                        for i in n.instr_addrs:
                            if i.addr != succ_addr and not stop:
                                new_node.instr_addrs = new_node.instr_addrs[1:]
                            else:
                                stop = True
                        new_node.instrs = len(new_node.instr_addrs)
                        # print(f"adding new Node({new_node.start_addr},{new_node.end_addr})")

                        if new_node.type == "call":
                            if arch.type == 'elf32-msp430':
                                indr_call = 'r' in node.instr_addrs[-1].arg
                                br_dest = clean_comment(arch, new_node.instr_addrs[-1].arg)
                            elif arch.type == "armv8-m33":
                                indr_call = arch.instrumentation_handle in new_node.instr_addrs[-1].arg
                                br_dest = "0x"+new_node.instr_addrs[-1].arg.split(' ')[0]
                                # print(f"call in node {node.start_addr}")
                                # print(br_dest)

                            if indr_call == True:
                                # handled later on...c
                                # print(f"indr_call={indr_call}, type:{node.type}, Node:({node.start_addr}, {node.end_addr}), instruction: {node.instr_addrs[-1].instr} {node.instr_addrs[-1].arg}")
                                cfg.indr_calls.append(new_node.start_addr)

                        break

                if new_node is not None:
                    if new_node.start_addr not in cfg.nodes: # check for dupes
                        cfg.nodes[new_node.start_addr] = new_node
                        cfg.num_nodes +=1



    return cfg

def update_parents(cfg):
    for key in cfg.nodes.keys():
        node = cfg.nodes[key]
        for sc in node.successors:
            try:
                cfg.nodes[sc].parents.append(node.start_addr)
            except KeyError:
                print(f'{sc} not in cfg')

def find_idr_call_site(args):
    call_reg, cfg, path, pid = args
    print(f"Using path: \n{path}\n")
    # print(f"Starting {pid}")
    debugFile = open('./logs/rda'+str(pid)+'.log', 'w')
    rda_emulator = Emulator(arch=cfg.arch, mode='rda', debugFile=debugFile, debug=True)
    n = 1
    i = 1
    total = 0
    for addr in path:
        total += len(cfg.nodes[addr].instr_addrs)
        for instr in cfg.nodes[addr].instr_addrs:
            # print(instr)
            # print(f"Path {pid}; Node {n}/{len(path)}; Instruction {i}/{total}  {instr} ")
            i += 1
            rda_emulator.step(instr)
        n += 1

    call_reg_val = hex(int(rda_emulator.get_reg(call_reg)))

    debugFile.close()
    return call_reg_val

def update_idr_call_sites_parallel(cfg, idr_call_node_addr):
    ## returns all possible paths (overapprox ret-addr values)
    # paths = find_paths(cfg, cfg.head, idr_call_node_addr)
    print(f'Running DFS until {idr_call_node_addr} is reached')    
    paths = dfs(cfg, cfg.head, idr_call_node_addr, ss=None, file=None)
    ## follow paths with ss, return only valid paths:
    # paths = get_valid_paths(cfg, paths)
    # print(f'Valid Paths: {len(paths)}')
    # for path in paths:
        # print(path)

    #'''
    if cfg.arch.type == 'elf32-msp430':
        call_reg = cfg.nodes[idr_call_node_addr].instr_addrs[-1].arg
    else:
        # need the second to last instru: mov sl, call_reg 
        call_reg = cfg.nodes[idr_call_node_addr].instr_addrs[-2].arg.split(', ')[1]
    print(f'Call_reg: {call_reg}')
    # a = input()

    # _ = system('clear')
    # print('-------------------------------------------')
    # print(' Emulating paths to determine call sites ' )
    # print('-------------------------------------------')

    # Create a multiprocessing Pool with the desired number of processes
    num_processes = multiprocessing.cpu_count()  # Use the number of CPU cores
    pool = multiprocessing.Pool(processes=num_processes)
    
    # Map the traverse_path function to the pool of processes and pass each path as an argument
    results = pool.map(find_idr_call_site, [(call_reg, cfg, paths[i], i) for i in range(0, len(paths))])

    # Close the pool to release resources
    pool.close()
    pool.join()

    if cfg.arch.type == 'armv8-m33':
        results = [hex(int(r, 16)^1) for r in results] # need to flip bit since arm store data as odd number
    
    #'''
    # results = [0]
    return results

def dfs(cfg, addr, end, path=None, ss=None, file=None):
    # print(f"starting {addr}")
    # a = input()
    
    if path == None:
        path = [addr]
    else:
        path.append(addr)

    if addr == end:
        return [path]

    if addr not in cfg.nodes.keys():
        return []

    if ss == None:
        ss = []

    # print(f"({addr}) path = {len(path)}")
    # a = input()
    paths = []
    if cfg.nodes[addr].type == 'ret':
        # for normal returns that had function before it
        if len(ss) > 0:
            successor_addr = ss[0]
            # print(f"(ret) {addr} --> {successor_addr}\t ss({len(ss)}) ", file=file)
            new_paths = dfs(cfg, successor_addr, end, path[:], ss[1:][:], file=file)
            # print(f"{addr} : new_paths {len(new_paths)}")
            for np in new_paths:
                paths.append(np)
        #else --> return
        # special case when loop exit is a return node, we ignore in this case since there is no associaed call

    elif cfg.nodes[addr].type == 'call':
        successor_addr = cfg.nodes[addr].successors[0]
        # print(f"({cfg.nodes[addr].type}) {addr} --> {successor_addr}", file=file)
        # add to stack if call    
        # debug = f"\t ss({len(ss)}) --> appending {cfg.nodes[addr].adj_instr} -- > "
        ss = [cfg.nodes[addr].adj_instr] + ss
        # debug += f"ss({len(ss)})"
        # print(debug)
        # a = input()
        new_paths = dfs(cfg, successor_addr, end, path[:], ss[:], file=file)
        # print(f"{addr} : new_paths {len(new_paths)}")
        for np in new_paths:
            paths.append(np)

    elif cfg.nodes[addr].type == 'uncond':
        for successor_addr in cfg.nodes[addr].successors:
            # detect loop via uncond jump; only need to worry about this for msp430
            if cfg.arch.type == 'elf32-msp430' and int(successor_addr, 16) <= int(addr, 16): #loop using dir jump
                # print(f"(uncond) (loop-enter) {addr} --> {successor_addr}\t ss({len(ss)}) ", file=file)
                path.append(successor_addr) #add loop entry once
                # print(f"\tappending {successor_addr} --> path : {path}", file=file)
                paths.append(path)
                
                # now continue dfs with 'loop exit'
                successor_addr = cfg.nodes[addr].adj_instr
                if successor_addr not in path:
                    new_paths = dfs(cfg, successor_addr, end, path[:], ss[:], file=file) # follow loop exit
                    for np in new_paths:
                        paths.append(np)

            else: #forward dir jump
                # print(f"({cfg.nodes[addr].type}) {addr} --> {successor_addr}", file=file)
                new_paths = dfs(cfg, successor_addr, end, path[:], ss[:], file=file)
                # print(f"{addr} : new_paths {len(new_paths)}")
                for np in new_paths:
                    paths.append(np)

    else:
        # need to check if successor 0 or 1 is a loop dest
        if int(cfg.nodes[addr].successors[0], 16) <= int(addr, 16):
            #successor 0 is loop, successor 1 is loop exit
            # print(f"(cond) (loop-enter) {addr} --> {cfg.nodes[addr].successors[0]}\t ss({len(ss)}) ", file=file)
            path.append(cfg.nodes[addr].successors[0]) #add loop entry once
            if cfg.nodes[addr].successors[1] not in path:
                # print(f"(cond) (loop-exit) {addr} --> {cfg.nodes[addr].successors[1]}\t ss({len(ss)}) ", file=file)
                # a = input()
                new_paths = dfs(cfg, cfg.nodes[addr].successors[1], end, path[:], ss[:], file=file) # follow loop exit
                for np in new_paths:
                    paths.append(np)
            else:
                paths.append(path)

        elif int(cfg.nodes[addr].successors[1], 16) <= int(addr, 16):
            #successor 1 is loop, successor 0 is loop exit
            # print(f"(cond) (loop-enter) {addr} --> {cfg.nodes[addr].successors[1]}\t ss({len(ss)}) ", file=file)
            path.append(cfg.nodes[addr].successors[1]) #add loop entry once
            if cfg.nodes[addr].successors[0] not in path:
                # print(f"(cond) (loop-exit) {addr} --> {cfg.nodes[addr].successors[0]}\t ss({len(ss)}) ", file=file)
                # a = input()                
                new_paths = dfs(cfg, cfg.nodes[addr].successors[0], end, path[:], ss[:], file=file) # follow loop exit
                for np in new_paths:
                    paths.append(np)
            else:
                paths.append(path)

        else: #neither --> this is a normal if-else
            for successor_addr in cfg.nodes[addr].successors:
                # print(f"({cfg.nodes[addr].type}) {addr} --> {successor_addr}\t ss({len(ss)}) ", file=file)
                new_paths = dfs(cfg, successor_addr, end, path[:], ss, file=file)
                # print(f"{addr} : new_paths {len(new_paths)}")
                for np in new_paths:
                    paths.append(np)

    # print(f"{addr} : returning {len(paths)}")
    return paths

def unique_end_nodes(cfg):
    unique_end_nodes = {}

    for addr, node in cfg.nodes.items():
        if node.end_addr in unique_end_nodes:
            print(f"{node.end_addr} in unique_end_nodes:")
            print(f"\t{node.start_addr} < {unique_end_nodes[node.end_addr].start_addr}")
            if int(node.start_addr,16) < int(unique_end_nodes[node.end_addr].start_addr,16):
                print(f"Discarding {unique_end_nodes[node.end_addr].start_addr}")
                print(f"Adding {node.start_addr}")
                unique_end_nodes[node.end_addr] = node
        else:
            unique_end_nodes[node.end_addr] = node

    unique = list(unique_end_nodes.values())
    # for u in unique:
    #     print(u.end_addr)
    return unique

def find_cfg_loop_nodes(cfg,asm_funcs):

    loops = []
    loop_dests = []
    ## first find all loops
    cfg_nodes = unique_end_nodes(cfg)
    # a = input()

    # Sorted loops: 
    # ['0x200464', '0x200484', '0x20067e', '0x200690', '0x2006a0', '0x2006b0', '0x300054', '0x30007c', '0x30009e']

    for node in cfg_nodes:
        # node = cfg.nodes[node_addr]
        if node.type == 'cond':
            # print(f"------- {node_addr} -------")
            # print(f"cond {node_addr}")
            if (int(node.successors[0],16) < int(node.end_addr,16) or int(node.successors[1],16) < int(node.end_addr,16)):
                if int(node.successors[0],16) < int(node.end_addr,16):
                    loop_dest = node.successors[0]
                else:
                    loop_dest = node.successors[1]

                loops.append(node.start_addr)
                # if loop_dest not in loop_dests:
                #     # print(f"appending {node_addr} and {loop_dest}")
                #     loops.append(node_addr)
                #     loop_dests.append(loop_dest)
                # else:
                #     print(f"{loop_dest} from {node_addr} in {loop_dests}")
        '''
        elif node.type == 'uncond':
            # print(f"trying uncond node {node_addr} to loop_nodes")
            if len(node.successors) == 1:
                if int(node.successors[0],16) < int(node.end_addr,16):
                    # print('\tadded!')
                    ## need to update adj instruction, which is traveled to by the cond br before it, to treat this as a loop node
                    if cfg.nodes[node_addr].instr_addrs[-1].instr == 'br':
                        cfg.nodes[node_addr].adj_instr = hex(int(node.end_addr, 16)+cfg.arch.double_instr_size)
                    elif cfg.nodes[node_addr].instr_addrs[-1].instr == 'jmp':
                        cfg.nodes[node_addr].adj_instr = hex(int(node.end_addr, 16)+cfg.arch.regular_instr_size)
                    # next append to list
                    loops.append(node_addr)
        '''

    ## now check instrs's from loop enter to loop exit to see if any other br instructions
    ### if none, add it to the empty loop
    empty_loops = []
    loops = sorted(loops)
    print("Sorted loops: ")
    print(loops)
    # a = input()

    empty_inner_loops = []
    for loop_node_addr in loops:
        loop_dest = '0x'+cfg.nodes[loop_node_addr].instr_addrs[-1].arg.split(' ')[0]
        # print(f"loop_node_addr: {loop_node_addr}")
        # print(f"loop dest: {loop_dest}")
        toAdd = True
        for func_addr in asm_funcs.keys():
            func = asm_funcs[func_addr]
            if int(loop_node_addr,16) >= int(func.start_addr,16) and int(loop_node_addr,16) <= int(func.end_addr,16):
                # now we are in the func that has the loop
                startMonitoring = False
                innerEmptyLoop = False
                for instr in func.instr_list:
                    isCall = instr.instr in cfg.arch.call_instrs or instr.instr in cfg.arch.indr_calls
                    isCond = instr.instr in cfg.arch.conditional_br_instrs
                    isRet = instr.instr in cfg.arch.return_instrs
                    if instr.addr in empty_loops:
                        innerEmptyLoop = True
                        naddrs = cfg.get_node(instr.addr)
                        print(f"instr.addr : {instr.addr}")
                        print(f"naddrs : {naddrs}")
                        print(f"empty_loops : {empty_loops}")
                        # empty_inner_loops.append(naddr)
                        # empty_loops.remove(naddr)
                        for n in naddrs:
                            if n in empty_loops:
                                empty_inner_loops.append(n)
                                empty_loops.remove(n)
                        # a = input()
                    if instr.addr == loop_dest:
                        # print("found loop dest!")
                        startMonitoring = True
                    elif startMonitoring and instr.addr == cfg.nodes[loop_node_addr].end_addr:
                        break
                    elif startMonitoring and (isCall or (isCond and not innerEmptyLoop) or isRet):
                        print(f'setting {loop_node_addr} to false at {instr.addr}: \t isCall:{isCall} isCond:{isCond} isRet:{isRet}')
                        toAdd = False
        if toAdd:
            empty_loops.append(loop_node_addr)

    return empty_loops, empty_inner_loops

def resolve_indr_jump_targets(cfg, indr_jump_node_addr, word_addrs=None, word_vals=None):
    # can leverage the fact that jump tables appear adjacent to the jump instruction...
    if cfg.arch.type == 'elf32-msp430':
        addr = cfg.nodes[indr_jump_node_addr].adj_instr
        # print(f"Starting search from {addr}")
        while cfg.nodes[addr].type == 'uncond':
            # print(f"adding {addr} to successors")
            cfg.nodes[indr_jump_node_addr].successors.append(addr)
            addr = cfg.nodes[addr].adj_instr
    else:
        node_addrs = sorted(list(cfg.nodes.keys()))
        
        ij_node_idx = node_addrs.index(indr_jump_node_addr)
        next_nodr_addr = node_addrs[ij_node_idx+1]
        # print(f"indr_jump_node_addr : {indr_jump_node_addr}")
        # print(f"ij_node_idx : {ij_node_idx}")
        # print(f"next_nodr_addr : {next_nodr_addr}\n")
        for i in range(0, len(word_addrs)):
            addr = word_addrs[i]
            val = word_vals[i]
            if int(addr, 16) >= int(indr_jump_node_addr, 16) and int(addr, 16) <= int(next_nodr_addr, 16):
                cfg.nodes[indr_jump_node_addr].successors.append(hex(int(val, 16)-1))
    # print(f"Updated indr jump successors ({len(cfg.nodes[indr_jump_node_addr].successors)}): \n{cfg.nodes[indr_jump_node_addr].successors}\n")

def create_cfg(arch, lines):
    # Instantiate CFG object
    cfg = CFG()
    cfg.arch = arch
    # Parse functions objdump file 
    # Detect the arch of the binary if not provided 
    arch,assembly_functions,label_addr_map = parse_asm_functions(arch,lines)
    
    function_file = open("logs/functions.log", "w")
    for key in assembly_functions:
        print(str(key)+" : "+str(assembly_functions[key]), file=function_file)
        for instr in assembly_functions[key].instr_list:
            print(f"\t{instr}", file=function_file)
        print("---------------------------", file=function_file)
    function_file.close()

    # Add map of labels to memory addrs to the cfg struct
    cfg.label_addr_map = label_addr_map

    # Parse nodes in each function
    cfg = parse_nodes(arch,assembly_functions,cfg)

    # for k in cfg.func_nodes.keys():
    #     print(f"{k}: {[n.start_addr for n in cfg.func_nodes[k]]}")
    # a = input()

    #Update the successors of all generated nodes 
    cfg = update_successors(arch,assembly_functions,cfg)
    print("Done update_successors")
    
    # print("Done update_parents")
    # f = open("logs/parents.log", "w")
    # for key in cfg.nodes.keys():      
    #     print(f"{key} : {cfg.nodes[key].parents}", file=f)
    #     print("---------------------------", file=f)
    # f.close()

    loop_nodes, empty_inner_loops = find_cfg_loop_nodes(cfg,assembly_functions)
    cfg.loop_nodes = loop_nodes
    cfg.inner_loop_nodes = empty_inner_loops
    print("empty inner loops:")
    for ei in empty_inner_loops:
        print(ei)
    print("\n EMPTY LOOP NODES")
    for addr in loop_nodes:
        print(addr)
    a = input()

    if cfg.arch.type == "elf32-msp430":
        cfg.head = cfg.label_addr_map['main']
    else: #arm
        cfg.head = cfg.label_addr_map['application']

    # print(f"CFG HEAD: {cfg.head}{type(cfg.head)}")
    if len(cfg.indr_calls) > 0:
        print(f"INDR CALLS: {cfg.indr_calls}")
        for addr in cfg.indr_calls:
            results = []
            print(f"Finding paths to {cfg.nodes[addr].instr_addrs[-1]}")
            results.extend(update_idr_call_sites_parallel(cfg, addr))
            results = set(results)
            print('Possible call sites:')
            for r in results:
                print(r)
            cfg.nodes[addr].successors = list(results)
            print(cfg.nodes[addr].successors)
            for ic_tgt in cfg.nodes[addr].successors:
                ret_node = assembly_functions[ic_tgt].return_node
                if ret_node is not None:
                    print(f"Adding {cfg.nodes[addr].adj_instr} to successors of {ic_tgt}")
                    ret_node.add_successor(cfg.nodes[addr].adj_instr)
    # a = input()
    
    f = open("objs/.words")
    word_addrs = []
    word_vals = []
    for line in f:
        addr, val = line.split(', ')
        word_addrs.append(addr)
        word_vals.append(val)
    f.close()

    if len(cfg.indr_jumps) > 0:
        for addr in cfg.indr_jumps:
            resolve_indr_jump_targets(cfg, addr, word_addrs, word_vals)

    # print(f"CFG LOOP NODES: {loop_nodes}")
    # a = input()

    #update parents for backwards tracing
    update_parents(cfg)

    return cfg, assembly_functions
    
