import itertools

def module_inputs_torch_nn_TransformerEncoderLayer(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    samples = [
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 16, 0.0),
            forward_input=FunctionInput(
                make_input((2, 3, 4))
            ),
            desc='relu_activation'
        ),
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 8, 0.0, F.gelu),
            forward_input=FunctionInput(
                make_input((2, 3, 4))
            ),
            desc='gelu_activation'
        ),
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 8, 0.0, bias=False),
            forward_input=FunctionInput(
                make_input((2, 3, 4))
            ),
            desc='no_bias'
        ), ]

    # Samples below are for validating the no-batch-dim support.
    key_padding_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool))
    attn_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool).expand((3, 3)))
    for src_mask, src_key_padding_mask, norm_first, batch_first, bias in \
            itertools.product(attn_masks, key_padding_masks, (True, False), (True, False), (True, False)):
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(d_model=4, nhead=2, dim_feedforward=8,
                                                dropout=0.0, batch_first=batch_first,
                                                norm_first=norm_first, bias=bias),
                forward_input=FunctionInput(
                    make_input((3, 4)), src_mask=src_mask, src_key_padding_mask=src_key_padding_mask
                ),
                reference_fn=partial(no_batch_dim_reference_fn,
                                     batch_first=batch_first, kwargs_to_batchify={'src_key_padding_mask': 0}),
                desc=f'no_batch_dim_batch_first_{batch_first}'
            ))

    # Samples below where we pass reference_fn are for validating the fast path,
    # since the fast path requires no_grad mode, we run the fast path in .eval()
    # and no_grad() in the reference_fn and verify that against the results in train mode.
    def fast_path_reference_fn(module, parameters, *args, **kwargs):
        if not module.training:
            raise AssertionError("Expected module.training to be True")
        module.train(False)
        with torch.no_grad():
            output = module(*args, **kwargs)
        module.train(True)
        return output

    if training:
        for norm_first, bias in itertools.product((True, False), (True, False)):
            samples.append(
                ModuleInput(
                    constructor_input=FunctionInput(
                        4, 2, 8, dropout=0.0, batch_first=True, norm_first=norm_first, bias=bias
                    ),
                    forward_input=FunctionInput(
                        make_input((2, 3, 4)),
                    ),
                    # fastpath doesn't run when bias=False
                    reference_fn=fast_path_reference_fn if bias else None,
                    desc=f'fastpath_{bias}_norm_first_{norm_first}'
                )
            )

    return samples

