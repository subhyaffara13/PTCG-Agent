
def aoti_load_package(
    path: FileLike, run_single_threaded: bool = False, device_index: int = -1
) -> AOTICompiledModel:
    """
    Loads the model from the PT2 package.

    If multiple models were packaged into the PT2, this will load the default
    model. To load a specific model, you can directly call the load API

    .. code-block:: python

        from torch._inductor.package import load_package

        compiled_model1 = load_package("my_package.pt2", "model1")
        compiled_model2 = load_package("my_package.pt2", "model2")

    Args:
        path: Path to the .pt2 package
        run_single_threaded (bool): Whether the model should be run without
            thread synchronization logic. This is useful to avoid conflicts with
            CUDAGraphs.
        device_index (int): The index of the device to which the PT2 package is
            to be loaded. By default, `device_index=-1` is used, which corresponds
            to the device `cuda` when using CUDA. Passing `device_index=1` would
            load the package to `cuda:1`, for example.
    """
    from torch._inductor.package import load_package

    return load_package(
        path, run_single_threaded=run_single_threaded, device_index=device_index
    )

