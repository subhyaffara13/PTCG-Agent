
def fake_tensor_prop(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    force_allow_non_fake_inputs: bool = False,
) -> torch._subclasses.FakeTensorMode:
    """
    If we can not detect fake mode from the context of inputs, create one.

    The created fake mode will be returned.
    """
    # Ensure that decomps that support symbolic shapes are used
    with enable_python_dispatcher():
        fake_mode = detect_fake_mode(example_inputs)
        if not fake_mode:
            fake_mode = torch._subclasses.FakeTensorMode(allow_non_fake_inputs=True)
            FakeTensorProp(gm, mode=fake_mode).propagate(*example_inputs)
        else:
            ctx = (
                contextlib.nullcontext()
                if not force_allow_non_fake_inputs
                else mock.patch.object(fake_mode, "allow_non_fake_inputs", True)
            )
            with ctx:  # type: ignore[attr-defined]
                FakeTensorProp(gm, mode=fake_mode).propagate_dont_convert_inputs(
                    *example_inputs
                )

    return fake_mode


def fake_tensor_prop(gm: GraphModule) -> None:
    inputs = []
    for node in gm.graph.find_nodes(op="placeholder", sort=False):
        fake_tensor = get_fake_tensor_from_node_arg(node)
        if fake_tensor is not None:
            inputs.append(fake_tensor)
        else:
            inputs.append(node)

    fake_mode = detect_fake_mode(inputs)
    FakeTensorProp(gm, mode=fake_mode).propagate_dont_convert_inputs(*inputs)

