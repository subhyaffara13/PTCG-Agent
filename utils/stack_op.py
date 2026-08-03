import functools
from typing import Any, Callable

def stack_op(fn: Callable[..., object]) -> Callable[..., Any]:
    nargs = len(inspect.signature(fn).parameters)
    fn_var = BuiltinVariable(fn)

    @functools.wraps(fn)
    def impl(self: InstructionTranslator, inst: Instruction) -> None:
        self.push(fn_var.call_function(self, self.popn(nargs), {}))

    return impl

