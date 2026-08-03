from typing import Any

def error_if_complex(func_name: str, args: Any, is_input: bool) -> None:
    flat_args = pytree.tree_leaves(args)
    for idx, arg in enumerate(flat_args):
        if isinstance(arg, torch.Tensor) and arg.dtype.is_complex:
            input_or_output = "inputs" if is_input else "outputs"
            err_msg = (
                f"{func_name}: Expected all {input_or_output} "
                f"to be real but received complex tensor at flattened input idx: {idx}"
            )
            raise RuntimeError(err_msg)

