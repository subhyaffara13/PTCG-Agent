
def copy_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")
    src = new_kwargs.pop("src")
    if inp._size != src._size:
        # try to recursively copy_ on unbound components to get around nested int mismatch
        # TODO: eventually do a direct copy when this is possible
        inp_comps = inp.unbind()
        inp_comp_shapes = [c.shape for c in inp_comps]
        src_comps = src.unbind()
        src_comp_shapes = [c.shape for c in src_comps]
        if inp_comp_shapes != src_comp_shapes:
            raise RuntimeError(
                "copy_(): expected compatible input and src shapes, but got: "
                f"{inp.shape} and {src.shape}"
            )
        for inp_comp, src_comp in zip(inp_comps, src_comps):
            inp_comp.copy_(src_comp)

    # AOTD allows mutations of inputs only, (not views of the inputs).
    # NJT.values() returns _values.detach() to workaround some issues.
    # To keep mutation in the graph, AOTD manually calls copy_ on the input (NJT).
    # Here we directly mutate self._values to not emit .detach() in the graph, which would make it non-compilable.
    inp._values.copy_(src._values)
    return inp

