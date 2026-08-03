from typing import Any

def to_fake_tensor(
    t: torch.Tensor, fake_mode: torch._subclasses.fake_tensor.FakeTensorMode
) -> Any:
    symbolic_context = None
    source = None
    if tracing_context := torch._guards.TracingContext.try_get():
        if t in tracing_context.tensor_to_context:
            symbolic_context = tracing_context.tensor_to_context[t]
            source = symbolic_context.tensor_source

    return fake_mode.from_tensor(
        t, static_shapes=False, symbolic_context=symbolic_context, source=source
    )

