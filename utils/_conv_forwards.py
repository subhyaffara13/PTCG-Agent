from typing import Optional

def _conv_forwards(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    transposed: bool,
    output_padding: list[int],
    groups: int,
    benchmark: bool,
    deterministic: bool,
    cudnn_enabled: bool,
    allow_tf32: bool,
) -> list[int]:
    return conv_forwards(
        input,
        weight,
        bias,
        stride,
        padding,
        dilation,
        transposed,
        output_padding,
        groups,
    )

