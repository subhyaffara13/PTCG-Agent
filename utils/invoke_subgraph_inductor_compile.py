import copy
from typing import Any

def invoke_subgraph_inductor_compile(
    gm, example_inputs, inductor_config_patches=None, **kwargs
):
    from torch._functorch._aot_autograd.runtime_wrappers import (
        SerializableCompiledFunction,
    )
    from torch._functorch._aot_autograd.utils import simple_wraps
    from torch._inductor import config
    from torch._inductor.compile_fx import compile_fx_inner
    from torch._inductor.standalone_compile import AOTCompiledArtifact

    # Used for testing only, should only be changed via _testing_capture_invoke_subgraph_inductor_compile_gms()
    if (
        torch._dynamo.testing._testing_invoke_subgraph_inductor_compile_captured_gms
        is not None
    ):
        torch._dynamo.testing._testing_invoke_subgraph_inductor_compile_captured_gms.append(
            copy.deepcopy(gm)
        )

    if inductor_config_patches is None:
        inductor_config_patches = {}
    compile_fn = config.patch(inductor_config_patches)(compile_fx_inner)
    compiled_fn_inner = compile_fn(gm, example_inputs)
    if not compiled_fn_inner._boxed_call:
        raise AssertionError(
            "compiled_fn_inner must have _boxed_call attribute set to True"
        )

    # Follow boxed calling convention
    @simple_wraps(compiled_fn_inner)
    def forward(*runtime_args: tuple[Any]):
        full_args = []
        full_args.extend(runtime_args)
        return compiled_fn_inner(full_args)

    # Just for convenience
    forward.zero_grad = gm.zero_grad  # type: ignore[attr-defined]
    forward.named_parameters = gm.named_parameters  # type: ignore[attr-defined]
    forward.named_buffers = gm.named_buffers  # type: ignore[attr-defined]

    # TODO: Do we need the post compile passes in _aot_stage2b_compile_forward_or_inference?
    # TODO: add a real serialize function for SerializableCompiledFunction like _cache_inference_info
    forward.serialize = SerializableCompiledFunction(forward, lambda: None)  # type: ignore[attr-defined]
    return AOTCompiledArtifact(forward)

