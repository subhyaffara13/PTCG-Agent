
def sample_inputs_unbind(op_info, device, dtype, requires_grad, **kwargs):
    # Note: we don't do any tests where we unbind along 0-length dims
    # because in that case unbind returns and empty tuple, and that breaks
    # some assumptions in some backward tests in test_ops.py
    shape_dims = (((S,), 0),
                  ((S, S), 0),
                  ((S, S), 1),
                  ((S, S), -1),
                  ((S, 0, S), 0),
                  ((S, S, S), 1),
                  )
    for shape, dim in shape_dims:
        yield SampleInput(make_tensor(shape, dtype=dtype, device=device,
                                      requires_grad=requires_grad),
                          args=(dim,))

