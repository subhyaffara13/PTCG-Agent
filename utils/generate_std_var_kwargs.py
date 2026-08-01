
def generate_std_var_kwargs(t: torch.Tensor, **kwargs):
    """Generates unbiased/correction kwargs for std/var operators"""
    yield ((), {'unbiased': True})
    yield ((), {'unbiased': False})

    # Currently, calling std with correction is only enabled when
    # both dim and keepdim are provided.
    if 'dim' in kwargs and 'keepdim' in kwargs:
        yield ((), {'correction': 0})
        yield ((), {'correction': 1})

        numel = torch.tensor(t.shape)[kwargs.get('dim')].prod()
        yield ((), {'correction': numel // 2})

