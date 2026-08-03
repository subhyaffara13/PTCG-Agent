from typing import Any, Callable

def make_leaf_function_wrappers(
    real_fn: Callable[..., Any],
    fake_fn: Callable[..., Any],
    captured_out_spec: list[pytree.TreeSpec | None],
) -> tuple[Callable[..., tuple[Any, ...]], Callable[..., tuple[Any, ...]]]:
    """Wrap real_fn and fake_fn to flatten outputs and capture the output TreeSpec.

    Both wrappers share the same captured output spec: the first call (typically
    fake_fn during tracing) records it, and subsequent calls verify consistency.
    The caller passes in a single-element list and reads captured_out_spec[0]
    after the wrappers have been called.

    Used by both the Dynamo path (_call_leaf_function in torch.py) and the
    make_fx path (_invoke_leaf_function_python in decorators.py).
    """

    def _wrap(fn: Callable[..., Any]) -> Callable[..., tuple[Any, ...]]:
        if len(captured_out_spec) != 1:
            raise RuntimeError(
                f"captured_out_spec must be a single-element list, got length {len(captured_out_spec)}"
            )

        def wrapper(*args: Any, **kwargs: Any) -> tuple[Any, ...]:
            out = fn(*args, **kwargs)

            flat_out, out_spec = pytree.tree_flatten(out)
            if captured_out_spec[0] is None:
                captured_out_spec[0] = out_spec
            elif captured_out_spec[0] != out_spec:
                raise AssertionError(
                    f"leaf_function output structure mismatch: "
                    f"expected {captured_out_spec[0]}, got {out_spec}. "
                    f"This can happen if the real function and fake function return "
                    f"different pytree structures (e.g., dict vs tuple, different number "
                    f"of elements). Ensure both functions return the same structure."
                )
            return tuple(flat_out)

        return wrapper

    return _wrap(real_fn), _wrap(fake_fn)

