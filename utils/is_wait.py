
def is_wait(node: IRNode | Operation | None) -> bool:
    from . import ir

    return type(node) is ir._WaitKernel

