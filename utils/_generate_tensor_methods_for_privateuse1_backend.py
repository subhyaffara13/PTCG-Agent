
def _generate_tensor_methods_for_privateuse1_backend(custom_backend_name: str) -> None:
    @property  # type: ignore[misc]
    def wrap_tensor_backend(self: torch.Tensor) -> bool:
        if has_torch_function_unary(self):
            # TODO mypy doesn't support @property, see: https://github.com/python/mypy/issues/6185
            return handle_torch_function(wrap_tensor_backend.__get__, (self,), self)  # type: ignore[attr-defined]
        return self.device.type == custom_backend_name

    _check_register_once(torch.Tensor, f"is_{custom_backend_name}")
    wrap_tensor_backend.fget.__name__ = f"is_{custom_backend_name}"  # type: ignore[attr-defined]
    setattr(torch.Tensor, f"is_{custom_backend_name}", wrap_tensor_backend)

    def wrap_tensor_to(
        self: torch.Tensor,
        device: int | torch.device | None = None,
        non_blocking=False,
        **kwargs,
    ) -> torch.Tensor:
        r"""Perform Tensor device conversion. Call the to operator implementation.

        .. note::
            If the ``self`` Tensor already
            has the correct :class:`torch.device`, then ``self`` is returned.
            Otherwise, the returned tensor is a copy of ``self`` with the desired :class:`torch.device`.

        Args:
            device (int, optional): if specified, all parameters will be copied to that device
            non_blocking (bool): If ``True`` and the source is in pinned memory,
                the copy will be asynchronous with respect to the host. Otherwise,
                the argument has no effect.
            **kwargs (dict): For compatibility, may contain the key ``memory_format`` argument.
        """
        if has_torch_function_unary(self):
            return handle_torch_function(
                wrap_tensor_to,
                (self,),
                self,
                device=device,
                non_blocking=False,
                **kwargs,
            )
        device_idx = _normalization_device(custom_backend_name, device)
        return self.to(
            device=torch.device(f"{custom_backend_name}:{device_idx}"),
            non_blocking=non_blocking,
            **kwargs,
        )

    _check_register_once(torch.Tensor, custom_backend_name)
    wrap_tensor_to.__name__ = custom_backend_name
    setattr(torch.Tensor, custom_backend_name, wrap_tensor_to)

