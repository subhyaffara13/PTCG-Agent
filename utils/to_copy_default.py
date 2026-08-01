
def to_copy_default(func, *args, **kwargs):
    from .nested_tensor import _tensor_symint_registry

    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    # don't change layout
    new_kwargs.pop("layout")

    new_values = func(inp._values, **new_kwargs)
    new_offsets = inp._offsets.to(device=new_values.device)
    new_lengths = None
    if inp._lengths is not None:
        new_lengths = inp._lengths.to(device=new_values.device)

    from torch._subclasses.fake_tensor import FakeTensor
    from torch._subclasses.functional_tensor import (
        FunctionalTensor,
        mb_unwrap_functional_tensor,
    )

    ragged_source = inp._offsets if inp._lengths is None else inp._lengths
    new_thing = new_offsets if new_lengths is None else new_lengths
    if isinstance(new_thing, (FakeTensor, FunctionalTensor)):
        # Temporary hack until we have the union find
        tgt = mb_unwrap_functional_tensor(new_thing)
        src = mb_unwrap_functional_tensor(ragged_source)
        # pyrefly: ignore[missing-attribute]
        tgt.nested_int_memo = src.nested_int_memo
    else:
        _tensor_symint_registry[new_thing] = _tensor_symint_registry[ragged_source]
    inp_kwargs = extract_kwargs(inp)
    inp_kwargs["offsets"] = new_offsets
    inp_kwargs["lengths"] = new_lengths

    output = NestedTensor(new_values, **inp_kwargs)
    return output

