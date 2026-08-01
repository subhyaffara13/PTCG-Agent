
def _is_custom_module_lstm(
    node: Node,
    named_modules: dict[str, torch.nn.Module],
    qconfig: QConfigAny = None,
    # QuantizeHandler, but we cannot include the type here due to circular imports
    qhandler: Any | None = None,
) -> bool:
    """
    Return whether this refers to the custom module LSTM flow.
    """
    mod = _get_module(node, named_modules)
    if qconfig is not None and qhandler is not None:
        if not isinstance(
            qhandler, torch.ao.quantization.fx.quantize_handler.QuantizeHandler
        ):  # type: ignore[attr-defined]
            raise AssertionError("qhandler must be a QuantizeHandler when provided")
        return (
            isinstance(mod, torch.nn.LSTM)
            and activation_is_statically_quantized(qconfig)
            and qhandler.is_custom_module()
        )
    else:
        return isinstance(mod, torch.ao.nn.quantizable.LSTM)

