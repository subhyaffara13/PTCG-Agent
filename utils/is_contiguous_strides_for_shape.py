
def is_contiguous_strides_for_shape(
    stride: Sequence[_IntLike], shape: Sequence[_IntLike]
) -> bool:
    expected_stride = 1
    expected_stride_max = 1
    for x, y in reversed(tuple(zip(shape, stride))):
        if x == 1:
            continue

        if not V.graph.sizevars.statically_known_equals(
            y, expected_stride
        ) and not V.graph.sizevars.statically_known_equals(y, expected_stride_max):
            return False

        expected_stride_max *= sympy.Max(1, x)
        expected_stride *= x

    return True

