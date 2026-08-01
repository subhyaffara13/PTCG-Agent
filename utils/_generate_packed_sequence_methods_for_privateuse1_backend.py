
def _generate_packed_sequence_methods_for_privateuse1_backend(
    custom_backend_name: str,
) -> None:
    # Generate PackedSequence Module attributes and methods depends on Tensor methods,
    # so we need to check whether Tensor methods is already registered.
    if not hasattr(torch.Tensor, f"is_{custom_backend_name}") or not hasattr(
        torch.Tensor, custom_backend_name
    ):
        raise RuntimeError(
            f"Can not automatically generate is_{custom_backend_name}() or "
            f"{custom_backend_name}() method for torch.nn.utils.rnn.PackedSequence."
            f"Because torch.Tensor doesn't has the method is_{custom_backend_name}()"
            f"or {custom_backend_name}()."
            f"For this error, you can try setting for_tensor=True."
        )

    @property  # type: ignore[misc]
    def wrap_tensor_backend(self: torch.nn.utils.rnn.PackedSequence) -> bool:
        return self.data.device.type == custom_backend_name

    _check_register_once(torch.nn.utils.rnn.PackedSequence, f"is_{custom_backend_name}")
    setattr(
        torch.nn.utils.rnn.PackedSequence,
        f"is_{custom_backend_name}",
        wrap_tensor_backend,
    )

    def wrap_module_to(
        self: torch.nn.utils.rnn.PackedSequence, *args, **kwargs
    ) -> torch.nn.utils.rnn.PackedSequence:
        r"""Move all model parameters and buffers to the custom device.

        This also makes associated parameters and buffers different objects. So
        it should be called before constructing optimizer if the module will
        live on device while being optimized.

        .. note::
            This method modifies the module in-place.

        Args:
            device (int, optional): if specified, all parameters will be copied to that device
        """
        ex = torch.tensor((), dtype=self.data.dtype, device=self.data.device).to(
            *args,
            **kwargs,
        )
        if ex.device.type == custom_backend_name:
            return self.to(*args, **kwargs)
        kwargs.update({"device": custom_backend_name})

        return self.to(*args, **kwargs)

    _check_register_once(torch.nn.utils.rnn.PackedSequence, custom_backend_name)
    setattr(torch.nn.utils.rnn.PackedSequence, custom_backend_name, wrap_module_to)

