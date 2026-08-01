
def _avg_pool(name, expand_size):
    @symbolic_helper.quantized_args(True, False, False, False, False, False, False)
    @symbolic_helper.parse_args("v", "is", "is", "is", "i", "i", "none")
    def symbolic_fn(
        g,
        input: _C.Value,
        kernel_size: Sequence[int],
        stride: Sequence[int],
        padding: int | Sequence[int],
        ceil_mode: int,
        count_include_pad: int,
        divisor_override=None,
    ):
        kernel_shape, strides, pads = _adjust_attributes_of_avg_pool(
            expand_size, kernel_size, stride, padding
        )

        result = g.op(
            "AveragePool",
            input,
            ceil_mode_i=ceil_mode,
            count_include_pad_i=count_include_pad,
            kernel_shape_i=kernel_shape,
            pads_i=pads,
            strides_i=strides,
        )

        return result

    return symbolic_fn


def _avg_pool(name, tuple_fn):
    @symbolic_helper.quantized_args(True)
    @symbolic_helper.parse_args("v", "is", "is", "is", "i", "i", "none")
    def symbolic_fn(
        g,
        input: _C.Value,
        kernel_size: Sequence[int],
        stride: Sequence[int],
        padding: int | Sequence[int],
        ceil_mode: int,
        count_include_pad: int,
        divisor_override=None,
    ):
        if not stride:
            stride = kernel_size
        padding = symbolic_helper._avgpool_helper(
            tuple_fn, padding, kernel_size, stride, divisor_override, name
        )
        if not isinstance(padding, tuple):
            raise AssertionError(f"Expected padding to be tuple, got {type(padding)}")
        adjusted_padding = padding
        # Although onnx::AvgPool provides count_include_pad,
        # The corner case of Average Pooling with ceil_mode on
        # PyTorch allows sliding window go off bound, which leads to
        # this accommodation.
        # More detail on https://github.com/pytorch/pytorch/issues/57178
        if count_include_pad:
            input = symbolic_helper._op_with_optional_float_cast(
                g,
                "Pad",
                input,
                pads_i=((0,) * 2 + padding) * 2,
                mode_s="constant",
                value_f=0.0,
                opset_before=11,
            )
            adjusted_padding = (0,) * len(padding)
        if ceil_mode:
            padding_ceil = get_pool_ceil_padding(input, kernel_size, stride, padding)
            adjusted_padding = adjusted_padding + tuple(
                a + b for (a, b) in zip(padding_ceil, adjusted_padding)
            )
        else:
            adjusted_padding = adjusted_padding * 2
        output = g.op(
            "AveragePool",
            input,
            kernel_shape_i=tuple_fn(kernel_size),
            strides_i=tuple_fn(stride),
            pads_i=adjusted_padding,
        )
        return output

    return symbolic_fn

