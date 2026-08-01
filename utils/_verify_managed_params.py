
def _verify_managed_params(module: nn.Module, params: list[nn.Parameter]) -> None:
    """
    Verify if the parameters are accepted by FSDP. The only restriction now
    is that the parameter cannot be a scalar tensor (param.shape == []).
    """
    for param in params:
        if len(param.shape) == 0:
            param_name = ""
            for name, param_ in module.named_parameters():
                if param is param_:
                    param_name = name
                    break
            if not param_name:
                raise AssertionError("Expected param_name to be set")
            raise ValueError(
                "FSDP doesn't support scalar parameters. "
                f"Change {param_name} to a 1D tensor with numel equal to 1."
            )

