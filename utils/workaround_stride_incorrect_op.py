import itertools
from typing import Any

def workaround_stride_incorrect_op(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    # This is a workaround for meta implementations with incorrect strides

    def is_symbolic(x: object) -> bool:
        if isinstance(x, FakeTensor):
            return x._has_symbolic_sizes_strides
        if isinstance(x, (torch.SymInt, torch.SymFloat, torch.SymBool)):
            return True
        return False

    # For static shapes, we can fall back to eager for the real strides
    if fake_mode.allow_fallback_kernels:
        require_dynamic = any(
            is_symbolic(x) for x in itertools.chain(args, kwargs.values())
        )
        if not require_dynamic:
            flat_args, args_spec = pytree.tree_flatten((args, kwargs))
            return run_fallback_kernel(
                fake_mode,
                func,
                flat_args,
                args_spec,
                # TODO: refactor to lambda so we don't instantiate extra errors before
                # calling
                RuntimeError("Cannot run fallback kernel for stride_incorrect_op"),
            )

    raise UnsupportedOperatorException(func)

