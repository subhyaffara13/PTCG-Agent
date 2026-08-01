
def inductor_lookup_seed(seeds, index):
    def inner_fn(_):
        return ops.load_seed(seeds.get_name(), index)

    return Pointwise.create(
        device=seeds.get_device(),
        dtype=seeds.get_dtype(),
        inner_fn=inner_fn,
        ranges=[],
    )

