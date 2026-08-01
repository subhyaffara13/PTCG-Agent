
def update_hidden_for_packed(cur_hidden, last_batch_size, batch_size, hiddens):
    if last_batch_size <= batch_size:
        raise AssertionError(
            f"last_batch_size ({last_batch_size}) must be > batch_size ({batch_size})"
        )
    hiddens.append(cur_hidden.narrow(0, batch_size, last_batch_size - batch_size))
    return cur_hidden.narrow(0, 0, batch_size)

