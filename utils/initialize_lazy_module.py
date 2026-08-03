from typing import Any

def initialize_lazy_module(
    tx: "InstructionTranslator",
    mod: torch.nn.Module,
    args: Sequence[VariableTracker],
    kwargs: dict[str, VariableTracker],
) -> None:
    """
    Fairly coupled helper used by NNModuleVariable and UnspecializedNNModuleVariable.

    Used to cause lazy module to be initialized (and delete its init hook) before tracing. Especially
    useful now that 'allowed' modules graph-break on hooks, calling this first ensures there is no hook
    by the time we trace __call__ and thus no graph-break for lazy allowed modules.
    """
    if hasattr(mod, "_initialize_hook"):

        def convert_to_fake(x: Any) -> Any:
            if is_namedtuple(x):
                return type(x)(*(convert_to_fake(elem) for elem in x))
            elif isinstance(x, dict):
                return {k: convert_to_fake(v) for k, v in x.items()}  # type: ignore[misc]
            elif isinstance(x, (list, tuple, set)):
                return type(x)(convert_to_fake(elem) for elem in x)
            elif isinstance(x, torch.fx.Proxy):
                return get_fake_value(x.node, tx)
            else:
                return x

        proxy_args, proxy_kwargs = proxy_args_kwargs(args, kwargs)
        fake_args = [convert_to_fake(arg) for arg in proxy_args]
        fake_kwargs = {k: convert_to_fake(v) for k, v in proxy_kwargs.items()}
        try:
            mod._infer_parameters(mod, fake_args, fake_kwargs)  # type: ignore[operator]
        except AttributeError:
            # Re-raise with the original error message from the AttributeError
            raise_observed_exception(
                AttributeError,
                tx,
                args=["AttributeError during lazy module initialization"],
            )

