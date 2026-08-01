
def _load_local(hubconf_dir, model, *args, **kwargs):
    r"""
    Load a model from a local directory with a ``hubconf.py``.

    Args:
        hubconf_dir (str): path to a local directory that contains a
            ``hubconf.py``.
        model (str): name of an entrypoint defined in the directory's
            ``hubconf.py``.
        *args (optional): the corresponding args for callable ``model``.
        **kwargs (optional): the corresponding kwargs for callable ``model``.

    Returns:
        a single model with corresponding pretrained weights.

    Example:
        >>> # xdoctest: +SKIP("stub local path")
        >>> path = "/some/local/path/pytorch/vision"
        >>> model = _load_local(
        ...     path,
        ...     "resnet50",
        ...     weights="ResNet50_Weights.IMAGENET1K_V1",
        ... )
    """
    with _add_to_sys_path(hubconf_dir):
        hubconf_path = os.path.join(hubconf_dir, MODULE_HUBCONF)
        hub_module = _import_module(MODULE_HUBCONF, hubconf_path)

        entry = _load_entry_from_hubconf(hub_module, model)
        model = entry(*args, **kwargs)

    return model

