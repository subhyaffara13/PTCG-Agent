
def update_hidden_for_packed_reverse(
    cur_hidden, last_batch_size, batch_size, inp_hidden
):
    if last_batch_size == batch_size:
        return cur_hidden
    if last_batch_size >= batch_size:
        raise AssertionError(
            f"last_batch_size ({last_batch_size}) must be < batch_size ({batch_size})"
        )
    return torch.concat(
        (
            cur_hidden,
            inp_hidden.narrow(0, last_batch_size, batch_size - last_batch_size),
        )
    )

