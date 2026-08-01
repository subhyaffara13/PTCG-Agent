
def _generate_module_methods_for_privateuse1_backend(custom_backend_name: str) -> None:
    # Generate Module attributes and methods depends on Tensor methods,
    # so we need to check whether Tensor methods is already registered.
    if not hasattr(torch.Tensor, custom_backend_name):
        raise RuntimeError(
            f"Can not automatically generate {custom_backend_name}() method for torch.nn.Module."
            f"Because torch.Tensor doesn't has the method {custom_backend_name}()."
            f"For this error, you can try setting for_tensor=True."
        )

    def wrap_module_to(
        # pyrefly: ignore [invalid-type-var]
        self: torch.nn.modules.module.T,
        device: int | torch.device | None = None,
    ) -> torch.nn.modules.module.T:  # pyrefly: ignore [invalid-type-var]
        r"""Move all model parameters and buffers to the custom device.

        This also makes associated parameters and buffers different objects. So
        it should be called before constructing optimizer if the module will
        live on device while being optimized.

        .. note::
            This method modifies the module in-place.

        Args:
            device (int, optional): if specified, all parameters will be copied to that device
        """
        # pyrefly: ignore [missing-attribute]
        return self._apply(lambda t: getattr(t, custom_backend_name)(device))

    _check_register_once(torch.nn.Module, custom_backend_name)
    setattr(torch.nn.Module, custom_backend_name, wrap_module_to)

