import copy
import sys

def remove_binary_store_slice(instructions: list[Instruction]) -> None:
    new_insts = []
    for inst in instructions:
        new_insts.append(inst)
        if inst.opname in ("BINARY_SLICE", "STORE_SLICE"):
            # new instruction
            if sys.version_info >= (3, 14) and inst.opname == "BINARY_SLICE":
                subscr_inst = create_binary_subscr()
            else:
                subscr_inst = create_instruction(inst.opname.replace("SLICE", "SUBSCR"))
            if inst.exn_tab_entry and inst.exn_tab_entry.end is inst:
                inst.exn_tab_entry.end = subscr_inst
            subscr_inst.exn_tab_entry = copy.copy(inst.exn_tab_entry)
            subscr_inst.positions = inst.positions
            # modify inst in-place to preserve jump target
            inst.opcode = dis.opmap["BUILD_SLICE"]
            inst.opname = "BUILD_SLICE"
            inst.arg = 2
            inst.argval = 2
            new_insts.append(subscr_inst)
    instructions[:] = new_insts

