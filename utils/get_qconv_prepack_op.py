from typing import Callable

def get_qconv_prepack_op(conv_op: Callable) -> Callable:
    prepack_ops = {
        torch.nn.functional.conv1d: torch.ops.quantized.conv1d_prepack,
        torch.nn.functional.conv2d: torch.ops.quantized.conv2d_prepack,
        torch.nn.functional.conv3d: torch.ops.quantized.conv3d_prepack,
        torch.nn.functional.conv_transpose1d: torch.ops.quantized.conv_transpose1d_prepack,
        torch.nn.functional.conv_transpose2d: torch.ops.quantized.conv_transpose2d_prepack,
        torch.nn.functional.conv_transpose3d: torch.ops.quantized.conv_transpose3d_prepack,
    }
    prepack_op = prepack_ops.get(conv_op)
    if prepack_op is None:
        raise AssertionError(f"Didn't find prepack op for {conv_op}")
    return prepack_op

