
def _update_sample(sample, new_kwargs):
    all_kwargs = dict(sample.kwargs)
    all_kwargs.update(new_kwargs)
    full_name = ", ".join([sample.name, *(f"{k}={v}" for (k, v) in new_kwargs.items())])
    return SampleInput(
        _clone(sample.input),
        args=sample.args,
        kwargs=all_kwargs,
        name=full_name,
    )

