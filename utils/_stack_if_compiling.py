
def _stack_if_compiling(x):
    if not torch.jit.is_scripting() and torch.compiler.is_compiling():
        return torch.stack(x)
    else:
        return x

