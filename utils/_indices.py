import itertools

def _indices(func, *args, **kwargs):
    # Assumes data is sparse
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=1, len_kwargs=0
    )
    data = _get_data(args[0]).indices()
    return MaskedTensor(data, torch.ones_like(data).bool())


def _indices(p, a, num_players):
  return [a if p_ == p else slice(None) for p_ in range(num_players)]


def _indices(ndims):
    """Returns ((axis0_src, axis0_dst), (axis1_src, axis1_dst), ... ) index pairs."""

    ind = _indices_for_axis()
    return itertools.product(ind, repeat=ndims)

