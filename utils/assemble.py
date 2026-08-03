import re
import sys

def assemble(instructions: list[Instruction], firstlineno: int) -> tuple[bytes, bytes]:
    """Do the opposite of dis.get_instructions()"""
    code: list[int] = []
    if sys.version_info >= (3, 11):
        lnotab, update_lineno = linetable_311_writer(firstlineno)
        num_ext = 0
        for i, inst in enumerate(instructions):
            if inst.opname == "EXTENDED_ARG":
                inst_size = 1
                num_ext += 1
                # copy positions from the actual instruction
                for j in (1, 2, 3):
                    if instructions[i + j].opname != "EXTENDED_ARG":
                        inst.positions = instructions[i + j].positions
                        break
            else:
                inst_size = instruction_size(inst) // 2 + num_ext
                num_ext = 0
            update_lineno(inst.positions, inst_size)
            num_ext = 0
            arg = inst.arg or 0
            code.extend((inst.opcode, arg & 0xFF))
            for _ in range(instruction_size(inst) // 2 - 1):
                code.extend((0, 0))
    else:
        lnotab, update_lineno, end = linetable_writer(firstlineno)

        for inst in instructions:
            if inst.starts_line is not None:
                update_lineno(inst.starts_line, len(code))
            arg = inst.arg or 0
            code.extend((inst.opcode, arg & 0xFF))

        end(len(code))

    return bytes(code), bytes(lnotab)


def assemble(result: _ods_ir.Type, levels: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], values: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return AssembleOp(result=result, levels=levels, values=values, loc=loc, ip=ip).result


def assemble(instrs):
    res = b""
    for inst in instrs:
        m = instre.match(inst)
        if not m or not m.group(1) in aCode_map:
            continue
        opcode, parmfmt = aCode_map[m.group(1)]
        res += struct.pack("B", opcode)
        if m.group(2):
            if parmfmt == 0:
                continue
            parms = [int(x) for x in re.split(r",\s*", m.group(2))]
            if parmfmt == -1:
                l = len(parms)
                res += struct.pack(("%dB" % (l + 1)), l, *parms)
            else:
                res += struct.pack(parmfmt, *parms)
    return res

