
def sample_inputs_trace(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       requires_grad=requires_grad, low=None, high=None)
    # Square, tall (rows > cols), wide (rows < cols), single row/col (#171704)
    for shape in ((S, S), (S + 2, S), (S, S + 2), (1, S), (S, 1)):
        yield SampleInput(make_arg(shape))

