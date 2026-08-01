
def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `ConditionalDetrFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = ConditionalDetrFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `DabDetrFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = DabDetrFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `DeformableDetrFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = DeformableDetrFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `Deimv2FrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = Deimv2FrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `DetrFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = DetrFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `DFineFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = DFineFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `GroundingDinoFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = GroundingDinoFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `MMGroundingDinoFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = MMGroundingDinoFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `PPDocLayoutV2FrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = PPDocLayoutV2FrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `PPDocLayoutV3FrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = PPDocLayoutV3FrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `RTDetrFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = RTDetrFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `RTDetrV2FrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = RTDetrV2FrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)


def replace_batch_norm(model):
    r"""
    Recursively replace all `torch.nn.BatchNorm2d` with `TableTransformerFrozenBatchNorm2d`.

    Args:
        model (torch.nn.Module):
            input model
    """
    for name, module in model.named_children():
        if isinstance(module, nn.BatchNorm2d):
            new_module = TableTransformerFrozenBatchNorm2d(module.num_features)

            if module.weight.device != torch.device("meta"):
                new_module.weight.copy_(module.weight)
                new_module.bias.copy_(module.bias)
                new_module.running_mean.copy_(module.running_mean)
                new_module.running_var.copy_(module.running_var)

            model._modules[name] = new_module

        if len(list(module.children())) > 0:
            replace_batch_norm(module)

