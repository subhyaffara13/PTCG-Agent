from typing import Any, Callable

def create_functional_call(
    mod: Any,
    params_spec: Any,
    params_len: int,
    store_orig_mod: bool = False,
    strict_out_tuple: bool = True,
) -> Callable[..., Any]:
    # Redundant with dynamo, but worth having in case this gets invoked elsewhere.
    # https://github.com/pytorch/pytorch/issues/103569

    @simple_wraps(mod)
    def functional_call(*args: Any, **kwargs: Any) -> Any:
        flat_params = args[:params_len]
        if isinstance(params_spec, TreeSpec):
            params = pytree.tree_unflatten(flat_params, params_spec)
        else:
            if not isinstance(params_spec, list):
                raise AssertionError(
                    f"expected params_spec to be a list, got {type(params_spec)}"
                )
            params = dict(zip(params_spec, flat_params))
        with (
            stateless._reparametrize_module(mod, params),
            maybe_disable_thunkify(),
        ):
            if isinstance(mod, torch.fx.GraphModule):
                if kwargs:
                    # Handle **kwargs. FX only natively supports positional
                    # arguments (through placeholders).
                    arg_list = list(args[params_len:])
                    arg_list.extend(list(kwargs.values()))
                    args = tuple(arg_list)
                else:
                    args = args[params_len:]

                with fx_traceback.preserve_node_meta(), warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore", "Anomaly Detection has been enabled."
                    )
                    with torch.autograd.detect_anomaly(check_nan=False):
                        fake_mode = detect_fake_mode()
                        if fake_mode is None:
                            raise AssertionError("fake_mode must not be None")
                        fake_mode.epoch += 1
                        out = PropagateUnbackedSymInts(mod).run(*args)
            else:
                out = mod(*args[params_len:], **kwargs)

        if strict_out_tuple and not isinstance(out, (tuple, list)):
            raise RuntimeError(
                "Graph output must be a (). This is so that we can avoid "
                "pytree processing of the outputs. Please change the module to "
                "have tuple outputs or use aot_module instead."
            )
        return out

    # Note [Preserving the nn module stack metadata during export non-strict mode]
    # This path is currently only used by the non-strict export flow,
    # where we cannot rely on dynamo to preserve nn stack metadata in our captured graph.
    # Instead, we stash the original user nn module here, and rely on `make_fx` to grab
    # this stashed module and use it to track nn module stack metadata
    if store_orig_mod and not hasattr(functional_call, "_orig_mod"):
        functional_call._orig_mod = mod  # type: ignore[attr-defined]

    return functional_call

