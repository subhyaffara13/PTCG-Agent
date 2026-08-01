
def call_delegate_cpu(
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
) -> list[torch.Tensor]:
    # FX creates this immutable_dict/list concept. Get rid of this.
    map_types: dict[type, type] = {
        torch.fx.immutable_collections.immutable_dict: dict,
        torch.fx.immutable_collections.immutable_list: list,
    }
    new_args = pytree.tree_map_only(
        tuple(map_types.keys()),
        lambda a: map_types[type(a)](a),
        weight_args + input_args,
        lambda a: isinstance(a, tuple(map_types.keys())),
    )
    has_fake_args = any(isinstance(arg, FakeTensor) for arg in new_args)
    if has_fake_args:
        # use stateless original_gm for tracing with fake tensors
        fake_out = original_gm(*new_args)
        return fake_out
    else:
        # use AOTI Runner for real tensors
        new_input_args = new_args[len(weight_args) :]
        if type(lowered_module).__name__ == "AOTInductorRunnerWrapper":
            return lowered_module(*new_input_args)  # type: ignore[misc]
        elif type(lowered_module).__name__ == "AOTInductorEPModule":
            return lowered_module(new_input_args)  # type: ignore[misc]
        else:
            raise RuntimeError(
                f"Unexpected lowered_module type: {type(lowered_module)}."
            )


def call_delegate_cpu(lowered_module, *args):
    # FX creates this immutable_dict/list concept. Get rid of this.
    map_types: dict[type, type] = {
        torch.fx.immutable_collections.immutable_dict: dict,
        torch.fx.immutable_collections.immutable_list: list,
    }
    new_args = pytree.tree_map_only(
        tuple(map_types.keys()),
        lambda a: map_types[type(a)](a),
        args,
        lambda a: isinstance(a, tuple(map_types.keys())),
    )
    return lowered_module.original_module.module()(*new_args)

