
def is_jit_model(
    model0: Any,
) -> TypeIs[
    torch.jit._trace.TopLevelTracedModule
    | torch.jit._script.RecursiveScriptModule
    | torch.jit.ScriptFunction[Any, Any]
    | torch.jit.ScriptModule
]:
    return isinstance(
        model0,
        (
            torch.jit._trace.TopLevelTracedModule,
            torch.jit._script.RecursiveScriptModule,
            torch.jit.ScriptFunction,
            torch.jit.ScriptModule,
        ),
    )

