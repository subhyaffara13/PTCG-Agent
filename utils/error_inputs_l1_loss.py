
def error_inputs_l1_loss(op_info, device, **kwargs):
    make = partial(make_tensor, device=device, dtype=torch.float32)

    # invalid reduction value
    yield ErrorInput(SampleInput(make(5, 4), args=(make(5, 4),),
                     kwargs={'reduction': 'abc'}),
                     error_type=ValueError,
                     error_regex='abc is not a valid value for reduction')
    # invalid input shapes
    yield ErrorInput(SampleInput(make(5, 4), args=(make(5,),)),
                     error_regex=(r'(Attempting to broadcast a dimension of length|'
                                  r'The size of tensor a \(4\) must match the '
                                  r'size of tensor b \(5\) at non-singleton '
                                  r'dimension 1)')
                     )

