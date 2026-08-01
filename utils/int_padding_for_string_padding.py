
def int_padding_for_string_padding(func, padding_style, dilation, kernel_size):
    def get_dilation(i):
        return dilation[i] if isinstance(dilation, tuple) else dilation

    if padding_style == "same":
        padding: list[int] = []
        # F.pad needs the padding in reverse order from what conv expects
        for i in range(conv_picker(func, 0, 1, 2), -1, -1):
            padding += conv_padding_for_same(get_dilation(i), kernel_size[i])
        return padding
    elif padding_style == "valid":
        return conv_picker(func, 2, 4, 6) * (0,)
    else:
        raise RuntimeError(
            f"got padding type of {padding_style}, only accept 'same' or 'valid'"
        )

