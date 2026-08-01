
def sample_inputs_embedding_bag(op_info, device, dtype, requires_grad, **kwargs):
    def make_input(shape):
        return make_tensor(shape, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_long_input(shape, *, low, high, noncontiguous=False):
        return make_tensor(shape, device=device, dtype=torch.long, low=low, high=high,
                           noncontiguous=noncontiguous)

    def make_per_sample_weight(flag, idx):
        # a tensor of float / double weights, or None
        # to indicate all weights should be taken to be 1
        if flag:
            return make_input(idx.shape)
        return None

    offsets = torch.tensor([0, 3], device=device, dtype=torch.long)
    for generate_per_sample_weight in (True, False):
        for mode in ('sum', 'mean', 'max'):
            # per_sample_weights is only supported for mode='sum' (got mode='****')
            if generate_per_sample_weight and mode in ('mean', 'max'):
                continue

            # 1-D index tensor
            idx = make_long_input((S,), low=0, high=M)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((M, S)), args=(idx,),
                              kwargs={'offsets': offsets, 'mode': mode,
                                      'per_sample_weights': per_sample_weights})

            idx = make_long_input((S,), low=0, high=M, noncontiguous=True)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((M, S)), args=(idx,),
                              kwargs={'offsets': offsets, 'mode': mode,
                                      'per_sample_weights': per_sample_weights})

            # bag with zero length
            idx = make_long_input((S,), low=0, high=M, noncontiguous=True)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((M, S)), args=(idx,),
                              kwargs={'offsets': torch.tensor([0, 0, 3], device=device, dtype=torch.long),
                                      'mode': mode,
                                      'per_sample_weights': per_sample_weights})

            # 2-D index tensor
            idx = make_long_input((S, S), low=0, high=M)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((M, S)), args=(idx,),
                              kwargs={'mode': mode, 'per_sample_weights': per_sample_weights})

            idx = make_long_input((S, S), low=0, high=M, noncontiguous=True)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((M, S)), args=(idx,),
                              kwargs={'mode': mode, 'per_sample_weights': per_sample_weights})

            # The gradient vector at `padding_idx` is not updated.
            # Negative padding_idx
            idx = make_long_input((6,), low=0, high=S)
            idx[0] = 4
            idx[4] = 4
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((S, S)), args=(idx,),
                              kwargs={'padding_idx': -1, 'offsets': offsets,
                                      'mode': mode, 'per_sample_weights': per_sample_weights},)

            idx = make_long_input((3, 3), low=0, high=S)
            # Positive padding_idx
            idx[0, 0] = 2
            idx[1, 1] = 2
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(make_input((S, S)), args=(idx,),
                              kwargs={'padding_idx': 2, 'mode': mode,
                                      'per_sample_weights': per_sample_weights},)

            idx = make_long_input((6, ), low=0, high=S)
            weights = make_input((S, S))
            offsets_ = torch.tensor([0, 3, 6], device=device, dtype=torch.long)
            per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
            yield SampleInput(weights, args=(idx,),
                              kwargs={'mode': mode, 'offsets': offsets_, 'include_last_offset': True},)

            if not requires_grad:
                # Following inputs return different gradient from the numerical gradient.
                # This is expected and relevant tests are present in `test_nn.py`.

                # Due to inplace renorming of weight, the numerical gradient doesn't match the
                # analytical gradient.
                idx = make_long_input((2, 2), low=0, high=S)
                weights = make_input((S, S)) * 2
                per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
                yield SampleInput(weights, args=(idx,),
                                  kwargs={'max_norm': 1., 'mode': mode,
                                          'per_sample_weights': per_sample_weights},)

                idx = make_long_input((6, ), low=0, high=S)
                weights = make_input((S, S)) * 2
                per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
                yield SampleInput(weights, args=(idx,),
                                  kwargs={'max_norm': 1., 'norm_type': 1.0,
                                          'mode': mode, 'offsets': offsets,
                                          'per_sample_weights': per_sample_weights},)

                if mode != 'max':
                    # Scale the gradient based on the inverse frequency of a particular index.
                    # Note : smax mode does not support sparse weights
                    idx = make_long_input((2, 2), low=0, high=S)
                    idx[0, 0] = 1
                    idx[0, 1] = 1
                    weights = make_input((S, S))
                    per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
                    yield SampleInput(weights, args=(idx,),
                                      kwargs={'scale_grad_by_freq': True, 'mode': mode,
                                              'per_sample_weights': per_sample_weights},)

                    # gradcheck not implemented for sparse tensors.
                    # Note : max mode does not support sparse weights
                    idx = make_long_input((6, ), low=0, high=S)
                    weights = make_input((S, S))
                    per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
                    yield SampleInput(weights, args=(idx,),
                                      kwargs={'sparse': True, 'offsets': offsets,
                                              'mode': mode, 'per_sample_weights': per_sample_weights})

                    idx = make_long_input((6, ), low=0, high=S)
                    idx[0] = 1  # freq more than 1
                    idx[1] = 1  # freq more than 1
                    idx[3] = 0  # padding_idx
                    weights = make_input((S, S)) * 2
                    per_sample_weights = make_per_sample_weight(generate_per_sample_weight, idx)
                    yield SampleInput(weights, args=(idx,),
                                      kwargs={'sparse': True, 'scale_grad_by_freq': True, 'padding_idx': 0,
                                              'max_norm': 1., 'offsets': offsets,
                                              'mode': mode, 'per_sample_weights': per_sample_weights})

