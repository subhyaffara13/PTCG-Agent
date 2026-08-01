
def error_inputs_margin_ranking_loss(op, device, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)
    # invalid reduction value.
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4), make_input(5, 4),), kwargs={'reduction': 'abc'}),
                     error_type=ValueError, error_regex='is not a valid value')
    # invalid input shapes
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4), make_input(5,),)),
                     error_regex='margin_ranking_loss : All input tensors should')

