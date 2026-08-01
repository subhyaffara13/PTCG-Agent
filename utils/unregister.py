
def unregister():
    """Unregister ONNX Runtime's built-in contrib ops."""
    for name in _registered_ops:
        try:
            torch.onnx.unregister_custom_op_symbolic(name, _OPSET_VERSION)
        except AttributeError:
            # The symbolic_registry module was removed in PyTorch 1.13.
            # We are importing it here for backwards compatibility
            # because unregister_custom_op_symbolic is not available before PyTorch 1.12
            from torch.onnx import symbolic_registry  # noqa: PLC0415

            namespace, kind = name.split("::")
            for version in symbolic_helper._onnx_stable_opsets:
                if version >= _OPSET_VERSION and symbolic_registry.is_registered_op(kind, namespace, version):
                    del symbolic_registry._registry[(namespace, version)][kind]

    # Also clean up gelu's multi-opset registrations (see register()).
    for opset in range(9, 21):
        with contextlib.suppress(Exception):
            torch.onnx.unregister_custom_op_symbolic("aten::gelu", opset)


def unregister(deprecation_id: str) -> None:
  if deprecation_id not in _registered_deprecations:
    raise ValueError(f"{deprecation_id=!r} not registered.")
  _registered_deprecations.pop(deprecation_id)


def unregister():
    from fsspec.implementations.http import HTTPFileSystem

    register_implementation("http", HTTPFileSystem, clobber=True)
    register_implementation("https", HTTPFileSystem, clobber=True)

