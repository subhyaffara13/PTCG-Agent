import math


def auto_pipeline_parallel(model: nn.Module, gpulist: list, sample_inputs: tuple):
    """Make the model executable across multiple GPUs."""

    def input_gpu_device_hook(mod, inputs, kwargs):
        modifyed_inputs = []
        first_dev = None
        for layer_input in inputs:
            if type(layer_input) is not torch.Tensor:
                modifyed_inputs.append(layer_input)
            elif hasattr(mod, "weight"):
                modifyed_inputs.append(layer_input.to(mod.weight.device))
            elif hasattr(mod, "parameters"):
                device = next(mod.parameters(), layer_input).device
                modifyed_inputs.append(layer_input.to(device))
            elif hasattr(next(mod.children(), None), "weight"):
                modifyed_inputs.append(layer_input.to(next(mod.children()).weight.device))
            elif first_dev is not None and layer_input.device != first_dev:
                modifyed_inputs.append(layer_input.to(first_dev))
            else:
                modifyed_inputs.append(layer_input)
            if first_dev is None:
                first_dev = modifyed_inputs[0].device
        for key, value in kwargs.items():
            if type(value) is torch.Tensor:
                kwargs[key] = value.to(first_dev)

        return (tuple(modifyed_inputs), kwargs)

    def move_layer_to_device_rurc(mod, dev):
        mod.to(dev)
        for layer in mod.named_children():
            move_layer_to_device_rurc(layer[1], dev)

    model = model.half()
    all_hooks = []
    all_hooks.append(model.register_forward_pre_hook(input_gpu_device_hook, with_kwargs=True))
    pre_fix = next(iter(model.named_children()))[0]
    for top_name, top_module in model.named_children():
        for name, module in top_module.named_children():
            all_hooks.append(module.register_forward_pre_hook(input_gpu_device_hook, with_kwargs=True))
            if type(module) in [torch.nn.ModuleList]:
                num_layers_on_each_gpu = math.floor(len(module) / len(gpulist))
                for idx, attn_layer in enumerate(module):
                    all_hooks.append(attn_layer.register_forward_pre_hook(input_gpu_device_hook, with_kwargs=True))

                    to_dev = gpulist[min(idx // num_layers_on_each_gpu, len(gpulist))]
                    attn_layer.to(to_dev)
                    move_layer_to_device_rurc(attn_layer, to_dev)
                    print(f"move {pre_fix}.{name}.{idx} to {to_dev}")
            else:
                module.to(gpulist[0])
                print(f"move {pre_fix}.{name} to {gpulist[0]}")
        if len(list(top_module.named_children())) == 0:
            top_module.to(gpulist[0])
            print(f"move {top_name} to {gpulist[0]}")

    with torch.no_grad():
        model(sample_inputs[0], attention_mask=sample_inputs[1])
    return model

