import sys

def instruction_size(inst: Instruction) -> int:
    import torch

    if sys.version_info >= (3, 11):
        return 2 * (torch._C._dynamo.eval_frame.py_opcode_caches[inst.opcode] + 1)
    return 2

