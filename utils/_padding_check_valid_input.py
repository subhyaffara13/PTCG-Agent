
def _padding_check_valid_input(input, padding, *, dim):
    torch._check(
        len(padding) == 2 * dim,
        lambda: f"padding size is expected to be {2 * dim}, but got: {len(padding)}",
    )

    input_dim = input.ndim

    is_batch_mode = input_dim == (dim + 2)

    valid_batch_mode = is_batch_mode
    valid_non_batch_mode = not is_batch_mode

    if is_batch_mode:
        # allow batch size of 0-dim.
        for d in range(1, input_dim):
            valid_batch_mode = valid_batch_mode and input.size(d) != 0
    else:
        for d in range(input_dim):
            valid_non_batch_mode = valid_non_batch_mode and input.size(d) != 0

    # allow empty batch size but not other dimensions.
    torch._check(
        valid_batch_mode or valid_non_batch_mode,
        lambda: (
            f"Expected {dim + 1}D or {dim + 2}D (batch mode) tensor with possibly 0 batch size "
            f"and other non-zero dimensions for input, but got: {input.shape}"
        ),
    )

