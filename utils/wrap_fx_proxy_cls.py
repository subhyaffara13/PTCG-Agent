from typing import Any

def wrap_fx_proxy_cls(
    target_cls: type[VTTypeAlias],
    tx: "InstructionTranslatorBase",
    proxy: Any,
    example_value: Any | None = None,
    subclass_type: type | None = None,
    **options: Any,
) -> VTTypeAlias:
    if example_value is None:
        out: VTTypeAlias = _wrap_fx_proxy(
            target_cls, tx, proxy, example_value, subclass_type, **options
        )
    elif isinstance(example_value, torch.Tensor):
        out = _wrap_fx_preexisting_tensor(
            target_cls, tx, proxy, example_value, subclass_type, **options
        )
    else:
        # This will skip tracing an op and recursively reinvoke wrap_fx_proxy_cls on supported
        # data structures. In essence this just handles tracing some other value which may
        # contain Fake Tensors or is otherwise proxyable.
        # pyrefly: ignore[bad-assignment]
        out = handle_traced_output(
            example_value, tx, proxy, options, subclass_type, target_cls
        )

    if (
        isinstance(
            out,
            (
                torch._dynamo.variables.TensorVariable,
                torch._dynamo.variables.SymNodeVariable,
            ),
        )
        and proxy.node.op != "placeholder"
    ):
        tx.output.current_tracer.record_proxyable_vt(out)
    return out

