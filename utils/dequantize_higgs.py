
def dequantize_higgs(model, current_key_name=None):
    """
    Dequantizes the HiggsLinear layers in the given model by replacing them with standard torch.nn.Linear layers.
    Args:
        model (torch.nn.Module): The model containing HiggsLinear layers to be dequantized.
        current_key_name (list, optional): A list to keep track of the current module names during recursion. Defaults to None.
    Returns:
        torch.nn.Module: The model with HiggsLinear layers replaced by torch.nn.Linear layers.
    """

    with torch.no_grad():
        for name, module in model.named_children():
            if current_key_name is None:
                current_key_name = []
            current_key_name.append(name)

            if isinstance(module, HiggsLinear):
                in_features = module.in_features
                out_features = module.out_features

                model._modules[name] = torch.nn.Linear(
                    in_features,
                    out_features,
                    bias=module.bias is not None,
                    device=module.scales.device,
                    dtype=module.scales.dtype,
                )

                model._modules[name].weight.data = module(
                    torch.eye(in_features, device=module.scales.device, dtype=module.scales.dtype)
                ).T.contiguous()

            if len(list(module.children())) > 0:
                _ = dequantize_higgs(
                    module,
                    current_key_name=current_key_name,
                )
            # Remove the last key for recursion
            current_key_name.pop(-1)
        return model

