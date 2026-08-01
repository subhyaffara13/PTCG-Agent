
def error_inputs_triplet_margin_loss(op_info, device, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)

    samples = (
        # input, args, kwargs, error_type, error_regex
        # invalid reduction
        (make_input(3, 4), (make_input(3, 4), make_input(3, 4)),
         dict(reduction="abc"),
         ValueError, "abc is not a valid value for reduction"),

        # invalid margin
        (make_input(3, 4), (make_input(3, 4), make_input(3, 4)),
         dict(margin=-1.0),
         ValueError, "margin must be greater than 0, got -1.0"),

        # shape mismatch
        (make_input(3, 5), (make_input(3, 4), make_input(3, 4)),
         {},
         RuntimeError,
         (r'(Attempting to broadcast a dimension of length|'
          r"The size of tensor a \(5\) must match the size of tensor b \(4\) "
          r"at non-singleton dimension 1)")),
        (make_input(3, 4), (make_input(3, 5), make_input(3, 4)),
         {},
         RuntimeError,
         (r'(Attempting to broadcast a dimension of length|'
          r"The size of tensor a \(4\) must match the size of tensor b \(5\) "
          r"at non-singleton dimension 1)")),
        (make_input(3, 4), (make_input(3, 4), make_input(3, 5)),
         {},
         RuntimeError,
         (r'(Attempting to broadcast a dimension of length|'
          r"The size of tensor a \(4\) must match the size of tensor b \(5\) "
          r"at non-singleton dimension 1)")),

        # different dimensions
        (make_input(3,), (make_input(3, 4), make_input(3, 4)),
         {},
         RuntimeError,
         (r"The anchor, positive, and negative tensors are expected to have "
          r"the same number of dimensions, but got: anchor 1D, positive 2D, "
          r"and negative 2D inputs")),
        (make_input(3, 4), (make_input(3,), make_input(3, 4)),
         {},
         RuntimeError,
         (r"The anchor, positive, and negative tensors are expected to have "
          r"the same number of dimensions, but got: anchor 2D, positive 1D, "
          r"and negative 2D inputs")),
        (make_input(3, 4), (make_input(3, 4), make_input(3,)),
         {},
         RuntimeError,
         (r"The anchor, positive, and negative tensors are expected to have "
          r"the same number of dimensions, but got: anchor 2D, positive 2D, "
          r"and negative 1D inputs")),
    )

    for input, args, kwargs, error_type, error_regex in samples:
        yield ErrorInput(SampleInput(input, args=args, kwargs=kwargs),
                         error_type=error_type, error_regex=error_regex)

