
def _fill_sample_kwargs(device, dtype, input):
    if dtype is torch.bool:
        value = True
    else:
        value = 3

    return ({'value': value}, {'value': value})

