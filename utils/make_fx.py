import functools
from typing import Any, Callable

def make_fx(
    f: Callable[..., Any],
    decomposition_table: Mapping[OpOverload, Callable[..., Any]] | None = None,
    tracing_mode: _TracingMode = "real",
    _allow_non_fake_inputs: bool = False,
    *,
    pre_dispatch: bool = False,
    record_module_stack: bool = False,
    _allow_fake_constant: bool = False,
    _error_on_data_dependent_ops: bool = True,
    record_stack_traces: bool = False,
    proxy_module_inputs: bool = False,
    _disable_torch_fn_metadata_mode: bool = False,
) -> Callable[..., GraphModule]:
    """
    Given a function f, return a new function which when executed with valid
    arguments to f, returns an FX GraphModule representing the set of operations that
    were executed during the course of execution.

    If record_stack_traces is True, the stack trace will be preserved on node.meta["stack_trace"]
    """

    if tracing_mode not in ["real", "fake", "symbolic"]:
        raise AssertionError(
            f"tracing_mode must be real/fake/symbolic, got {tracing_mode}"
        )

    from torch._inductor import config

    make_fx_tracer = _MakefxTracer(
        decomposition_table,
        tracing_mode,
        _allow_non_fake_inputs,
        pre_dispatch,
        record_module_stack,
        _allow_fake_constant,
        _error_on_data_dependent_ops,
        record_stack_traces=record_stack_traces
        or config.trace.provenance_tracking_level == 1,
        proxy_module_inputs=proxy_module_inputs,
        _disable_torch_fn_metadata_mode=_disable_torch_fn_metadata_mode,
    )

    @functools.wraps(f)
    def wrapped(*args: object) -> GraphModule:
        return make_fx_tracer.trace(f, *args)

    return wrapped

