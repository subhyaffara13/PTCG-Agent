from typing import Callable

def _onnx_op(
    op_type: str, opset_version: int, fake_impl: Callable[_P, _R]
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """Decorator to register an ONNX operator with a custom implementation."""

    def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
        overload = f"opset{opset_version}"
        torch_op = torch.library.custom_op(
            f"onnx::{op_type}.{overload}", mutates_args=()
        )(func)
        ONNX_ATEN_DECOMP_TABLE[getattr(getattr(torch.ops.onnx, op_type), overload)] = (
            func  # type: ignore[assignment]
        )
        torch_op.register_fake(fake_impl)
        return torch_op  # type: ignore[return-value]

    return decorator

