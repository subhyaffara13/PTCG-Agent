
def module_inputs_torch_nn_TransformerDecoderLayer(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    samples = [
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 16, 0.0),
            forward_input=FunctionInput(
                make_input((2, 3, 4)), make_input((2, 3, 4))
            ),
            desc='relu_activation'
        ),
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 8, 0.0, F.gelu),
            forward_input=FunctionInput(
                make_input((2, 3, 4)), make_input((2, 3, 4))
            ),
            desc='gelu_activation'
        ),
        ModuleInput(
            constructor_input=FunctionInput(4, 2, 8, 0.0, bias=False),
            forward_input=FunctionInput(
                make_input((2, 3, 4)), make_input((2, 3, 4))
            ),
            desc='no_bias'
        ), ]

    key_padding_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool))
    attn_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool).expand((3, 3)))
    for tgt_mask, tgt_key_padding_mask, norm_first, bias, batch_first in \
            itertools.product(attn_masks, key_padding_masks, (True, False), (True, False), (True, False)):
        # Using same mask for tgt and memory
        memory_mask = tgt_mask
        memory_key_padding_mask = tgt_key_padding_mask
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(d_model=4, nhead=2, dim_feedforward=8,
                                                dropout=0.0, batch_first=batch_first,
                                                norm_first=norm_first, bias=bias),
                forward_input=FunctionInput(
                    make_input((3, 4)), make_input((3, 4)), tgt_mask=tgt_mask, memory_mask=memory_mask,
                    tgt_key_padding_mask=tgt_key_padding_mask, memory_key_padding_mask=memory_key_padding_mask
                ),
                reference_fn=partial(no_batch_dim_reference_fn,
                                     batch_first=batch_first,
                                     kwargs_to_batchify={'tgt_key_padding_mask': 0, 'memory_key_padding_mask': 0}),
                desc=f'no_batch_dim_batch_first_{batch_first}'
            ))
        src, tgt = make_input((2, 3, 4)), make_input((2, 3, 4))
        if not batch_first:
            src, tgt = src.transpose(0, 1), tgt.transpose(0, 1)
        if tgt_key_padding_mask is not None:
            memory_key_padding_mask, tgt_key_padding_mask = (tgt_key_padding_mask.expand(2, 3),) * 2
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(d_model=4, nhead=2, dim_feedforward=8,
                                                dropout=0.0, batch_first=batch_first,
                                                norm_first=norm_first, bias=bias),
                forward_input=FunctionInput(
                    src, tgt, tgt_mask=tgt_mask, memory_mask=memory_mask,
                    tgt_key_padding_mask=tgt_key_padding_mask, memory_key_padding_mask=memory_key_padding_mask
                ),
                desc=f'norm_first_{norm_first}_batch_first_{batch_first}_bias_{bias}'
            ))

    return samples

