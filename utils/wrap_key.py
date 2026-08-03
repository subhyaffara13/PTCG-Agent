import functools
from typing import Callable

def wrap_key(
    f: Callable[[Unpack[_Ts]], R],
    tensors: tuple[Unpack[_Ts]],
    tracer: _ProxyTracer,
    pre_dispatch: bool,
) -> Callable[_P, R]:
    flat_tensors, _tensors_spec = pytree.tree_flatten(tensors)

    @functools.wraps(f)
    def wrapped(*proxies: _P.args, **_unused: _P.kwargs) -> R:
        nonlocal tensors

        flat_proxies, _proxies_spec = pytree.tree_flatten(proxies)
        if len(flat_proxies) != len(flat_tensors):
            raise AssertionError(
                f"Expected same length: {len(flat_proxies)} vs {len(flat_tensors)}"
            )
        with disable_proxy_modes_tracing() as m:
            if not isinstance(m, ProxyTorchDispatchMode):
                raise AssertionError(f"Expected ProxyTorchDispatchMode, got {type(m)}")
            track_tensor_tree(flat_tensors, flat_proxies, constant=None, tracer=tracer)

        if getattr(tracer, "proxy_module_inputs", False):
            tensors = [  # type: ignore[assignment, var-annotated]
                p if isinstance(t, torch.nn.Module) else t
                for t, p in zip(tensors, proxies)  # type: ignore[arg-type]
            ]

        def get_tensor_proxy_slot(t: Tensor) -> Tensor | Proxy:
            return get_proxy_slot(t, tracer, t, lambda x: x.proxy)  # type: ignore[attr-defined]

        out = f(*tensors)  # type:ignore[call-arg]
        out = pytree.tree_map_only(Tensor, get_tensor_proxy_slot, out)
        out = pytree.tree_map_only(
            _AnyScriptObject, lambda t: get_proxy_slot(t, tracer, t, lambda x: x), out
        )
        out = pytree.tree_map_only(
            OpaqueBase, lambda t: get_proxy_slot(t, tracer, t, lambda x: x), out
        )

        def get_sym_proxy_slot(t: PySymType) -> Proxy:
            return get_proxy_slot(t, tracer).force()

        out = pytree.tree_map_only(py_sym_types, get_sym_proxy_slot, out)
        return out

    return wrapped

