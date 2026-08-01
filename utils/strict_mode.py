
def strict_mode(callable, operands):
    if torch.compiler.is_dynamo_compiling():
        return strict_mode_op(callable, operands)

    from torch._higher_order_ops.utils import _hop_compile_and_call

    return _hop_compile_and_call(strict_mode_op, (callable, operands))

