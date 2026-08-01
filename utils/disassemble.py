
def disassemble(ret_levels: _Sequence[_ods_ir.Type], ret_values: _ods_ir.Type, lvl_lens: _Sequence[_ods_ir.Type], val_len: _ods_ir.Type, tensor: _ods_ir.Value[_ods_ir.RankedTensorType], out_levels: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], out_values: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, DisassembleOp]:
  op = DisassembleOp(ret_levels=ret_levels, ret_values=ret_values, lvl_lens=lvl_lens, val_len=val_len, tensor=tensor, out_levels=out_levels, out_values=out_values, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def disassemble(aCode):
    codelen = len(aCode)
    pc = 0
    res = []
    while pc < codelen:
        opcode = byteord(aCode[pc : pc + 1])
        if opcode > len(aCode_info):
            instr = aCode_info[0]
        else:
            instr = aCode_info[opcode]
        pc += 1
        if instr[1] != 0 and pc >= codelen:
            return res
        if instr[1] == -1:
            count = byteord(aCode[pc])
            fmt = "%dB" % count
            pc += 1
        elif instr[1] == 0:
            fmt = ""
        else:
            fmt = instr[1]
        if fmt == "":
            res.append(instr[0])
            continue
        parms = struct.unpack_from(fmt, aCode[pc:])
        res.append(instr[0] + "(" + ", ".join(map(str, parms)) + ")")
        pc += struct.calcsize(fmt)
    return res

