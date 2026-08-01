
def test_set_offsets_late():
    identity = mtransforms.IdentityTransform()
    sizes = [2]

    null = mcollections.CircleCollection(sizes=sizes)

    init = mcollections.CircleCollection(sizes=sizes, offsets=(10, 10))

    late = mcollections.CircleCollection(sizes=sizes)
    late.set_offsets((10, 10))

    # Bbox.__eq__ doesn't compare bounds
    null_bounds = null.get_datalim(identity).bounds
    init_bounds = init.get_datalim(identity).bounds
    late_bounds = late.get_datalim(identity).bounds

    # offsets and transform are applied when set after initialization
    assert null_bounds != init_bounds
    assert init_bounds == late_bounds

