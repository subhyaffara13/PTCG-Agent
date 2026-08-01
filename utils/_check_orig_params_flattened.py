
def _check_orig_params_flattened(
    fsdp_module,
    ignored_params: set[nn.Parameter],
) -> None:
    """
    Check that original parameters in ``fsdp_module`` have been flattened.

    The flattened parameters are made
    invisible to ``named_parameters()`` for the module hierarchy rooted at
    ``fsdp_module``. This should be called as a sanity check after flattening
    the wrapped module's parameters.
    """
    for param_name, param in _named_parameters_with_duplicates(fsdp_module):
        if param not in ignored_params and not _is_fsdp_flattened(param):
            raise RuntimeError(
                f"Found an unflattened parameter: {param_name}; "
                f"{param.size()} {param.__class__}"
            )

