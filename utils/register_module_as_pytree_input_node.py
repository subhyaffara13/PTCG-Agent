import copy
import json
from typing import Any

def register_module_as_pytree_input_node(cls: type[torch.nn.Module]) -> None:
    """
    Registers a module as a valid input type for :func:`torch.export.export`.

    Args:
        mod: the module instance
        serialized_type_name: The serialized name for the module. This is
        required if you want to serialize the pytree TreeSpec containing this
        module.

    Example::

        import torch


        class Module(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(3, 3)

            def forward(self, x):
                return self.linear(x)


        torch._export.utils.register_module_as_pytree_node(InputDataClass)


        class Mod(torch.nn.Module):
            def forward(self, x, m):
                return m(x) + x


        ep = torch.export.export(Mod(), (torch.randn(3), Module()))
        print(ep)

    """
    if not issubclass(cls, torch.nn.Module):
        raise AssertionError(f"expected nn.Module subclass, got {cls}")

    import weakref

    class PrototypeModule(weakref.ref):
        def __init__(self, m, *args, **kwargs):
            super().__init__(m, *args, **kwargs)  # type: ignore[call-arg]
            if not isinstance(m, torch.nn.Module):
                raise AssertionError(f"expected nn.Module, got {type(m).__name__}")
            if hasattr(self, "_proto_cls"):
                raise AssertionError("_proto_cls should not be set")
            self._proto_cls = cls

        def __eq__(self, other):
            return self._proto_cls == other._proto_cls

        def __deepcopy__(self, memo):
            return PrototypeModule(self())

    def default_flatten_fn(obj: Any) -> tuple[list[Any], Context]:
        named_parameters = dict(obj.named_parameters())
        named_buffers = dict(obj.named_buffers())
        params_buffers = {**named_parameters, **named_buffers}
        return list(params_buffers.values()), [
            list(params_buffers.keys()),
            PrototypeModule(obj),
        ]

    def default_unflatten_fn(values: Iterable[Any], context: Context) -> Any:
        flat_names, ref = context
        if ref is None or ref() is None:
            raise RuntimeError("Module has been garbage collected")
        obj = ref()
        if flatten_fn is None:
            raise AssertionError("flatten_fn should not be None")
        flattened, _ = flatten_fn(obj)

        # NOTE: This helper function will replicate an nn.Module in the exactly same
        #       structure to be used together with _reparameterize_module. This will
        #       create a clone of the module with the new parameters and buffers without
        #       affecting the original module.
        def copy_module(mod: torch.nn.Module):
            ret = copy.copy(mod)
            ret.__dict__ = {copy.copy(k): copy.copy(v) for k, v in mod.__dict__.items()}
            for name, child in ret.named_children():
                setattr(ret, name, copy_module(child))
            return ret

        if any(v is not o for v, o in zip(values, flattened)):
            with torch.nn.utils.stateless._reparametrize_module(
                obj, dict(zip(flat_names, values)), tie_weights=True, strict=True
            ):
                ret = copy_module(obj)
        else:
            ret = obj
        return ret

    def default_flatten_fn_with_keys(obj: Any) -> tuple[list[Any], Context]:
        flattened, [flat_names, *args] = flatten_fn(obj)  # type: ignore[misc]
        return [(MappingKey(k), v) for k, v in zip(flat_names, flattened)], [
            flat_names,
            *args,
        ]

    flatten_fn = default_flatten_fn
    unflatten_fn = default_unflatten_fn

    serialized_type_name = cls.__module__ + "." + cls.__qualname__

    def to_dumpable_context(context):
        keys, *_ = context
        return json.dumps([keys, *([None] * len(_))])

    def from_dumpable_context(dumpable):
        s = json.loads(dumpable)
        s[1] = PrototypeModule(torch.nn.Module())
        return s

    _register_pytree_node(
        cls,
        flatten_fn,
        unflatten_fn,
        serialized_type_name=serialized_type_name,
        flatten_with_keys_fn=default_flatten_fn_with_keys,
        to_dumpable_context=to_dumpable_context,
        from_dumpable_context=from_dumpable_context,
    )

    def default_flatten_fn_spec(obj, spec) -> list[Any]:
        flats, context = flatten_fn(obj)
        if context != spec.context:
            raise AssertionError(f"context mismatch: {context} != {spec.context}")
        return flats

    register_pytree_flatten_spec(
        cls,
        default_flatten_fn_spec,
    )

