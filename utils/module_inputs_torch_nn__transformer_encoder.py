
def module_inputs_torch_nn_TransformerEncoder(module_info, device, dtype, requires_grad, training, **kwargs):
    # Reuse the TransformerEncoderLayer samples since the forward args are nearly the same.
    samples = []
    for layer_module_input in module_inputs_torch_nn_TransformerEncoderLayer(
            None, device, dtype, requires_grad, training):
        # Construct a TransformerEncoderLayer object to pass to TransformerEncoder.
        l_args, l_kwargs = (layer_module_input.constructor_input.args,
                            layer_module_input.constructor_input.kwargs)
        l_kwargs['device'] = device
        l_kwargs['dtype'] = dtype
        encoder_layer = torch.nn.TransformerEncoderLayer(*l_args, **l_kwargs)
        num_layers = 2
        # Note: TransformerEncoderLayer takes a "src_mask" while
        # TransformerEncoder takes a "mask"; rename kwarg appropriately.
        forward_input = layer_module_input.forward_input
        if 'src_mask' in forward_input.kwargs:
            forward_input.kwargs['mask'] = forward_input.kwargs['src_mask']
            del forward_input.kwargs['src_mask']
        samples.append(ModuleInput(
            constructor_input=FunctionInput(encoder_layer, num_layers),
            forward_input=forward_input,
            desc=layer_module_input.desc
        ))
    return samples

