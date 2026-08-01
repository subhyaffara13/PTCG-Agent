
def _flatten_optim_state_dict(state_dict: OptimizerStateType) -> dict[str, ValueType]:
    """
    This API flattens the optimizer state_dict to support optimizer resharding for
    MPMD, e.g., pipeline parallelism.

    Without the API, the original optimizer state_dict looks like:
    {
        "state": {
            "layer1.weight": {
                "step": 10, "exp_avg": SomeTensor, "exp_avg_sq": SomeTensor
            },
            "layer2.weight": {
                "step": 10, "exp_avg": SomeTensor, "exp_avg_sq": SomeTensor
            },
        },
        "param_groups": [
            {
                "lr": 0.0,
                "betas": (0.9, 0.95), ...,
                "params": ["layer1.weight", "layer2.weight"]
            }
        ]
    }

    With this API, the optimizer state_dict looks like:
    {
        "state.layer1.weight.step": 10,
        "state.layer2.weight.step": 10,
        "state.layer1.weight.exp_avg": SomeTensor,
        "state.layer2.weight.exp_avg": SomeTensor,
        "state.layer1.weight.exp_avg_sq": SomeTensor,
        "state.layer2.weight.exp_avg_sq": SomeTensor,
        "param_groups.layer1.weight.lr": 0.1,
        "param_groups.layer2.weight.lr": 0.1,
        "param_groups.layer1.weight.betas": (0.9, 0.95),
        "param_groups.layer2.weight.betas": (0.9, 0.95),
    }

    The "state" section supports arbitrary levels of nesting for optimizers like Shampoo.
    """

    def _flatten_state_nested_dict(
        nested_dict: dict[str, Any], prefix: str
    ) -> dict[str, ValueType]:
        """
        Recursively flatten a nested dictionary with dot-separated keys.

        Args:
            nested_dict: The dictionary to flatten
            prefix: The prefix to prepend to all keys

        Returns:
            Flattened dictionary with dot-separated keys
        """
        flattened: dict[str, ValueType] = {}

        for key, value in nested_dict.items():
            # Convert all keys to strings for flattening
            str_key = str(key)
            full_key = f"{prefix}.{str_key}" if prefix else str_key

            if isinstance(value, dict):
                # Recursively flatten nested dictionaries
                flattened.update(_flatten_state_nested_dict(value, full_key))
            else:
                # Base case: store the value with the flattened key
                _raise_if_type_not_supported(value)
                flattened[full_key] = value

        return flattened

    def _raise_if_type_not_supported(v):
        if not isinstance(v, (torch.Tensor, int, float, dict)):
            raise NotImplementedError(
                "Flattening optimizer state_dict only supports "
                "tensor, int, float, dict states now. "
                f"Type is {type(v)}."
            )

    ret: dict[str, ValueType] = {}

    # Handle the "state" section with recursive flattening
    for fqn, state in cast(DictValueType, state_dict[_STATE]).items():
        state_prefix = f"{_STATE}.{fqn}"
        ret.update(
            _flatten_state_nested_dict(cast(dict[str, Any], state), state_prefix)
        )

    # Handle the "param_groups" section with two-level flattening
    for param_group in cast(ListDictValueType, state_dict[_PG]):
        fqns = param_group.pop(_PARAMS)
        for fqn in cast(list[str], fqns):
            for k, v in param_group.items():
                ret[f"{_PG}.{fqn}.{k}"] = v

    return ret


def _flatten_optim_state_dict(
    optim_state_dict: dict[str, Any],
    model: nn.Module,
    use_orig_params: bool = False,
    optim: torch.optim.Optimizer | None = None,
    rank0_only: bool = False,
    group: dist.ProcessGroup | None = None,
) -> dict[str, Any]:
    """
    Flattens the full optimizer state dict, still keying by unflattened parameter
    names.

    If ``use_orig_params`` is True, each rank will have all FSDP-managed
    parameters but some of these parameters may be empty due to the sharding.
    For a regular optim.Optimizer, states for those empty parameters will
    not be initialized. So, when aggregating the FQNs across ranks, no assert
    will be raised on a rank even if it does not have all the states -- it is
    valid and FSDP know how to aggregate them. However, FSDP has to ignore
    handling those parameters that are not managed by FSDP and do not exist on
    the local rank -- it is managed by other parallelism and FSDP does not
    know ho to handle/aggregate them.

    Note that ``_flatten_tensor_optim_state`` does not need ``optim`` to
    flatten/shard the state. However, NamedOptimizer and KeyedOptimizer require
    all the states even if the corresponding parameters are empty. To this end,
    ``optim`` will be used to get the initial state of the empty parameters.
    ``optim`` should only be non-None if the ``optim` is KeyedOptimizer or
    NamedOptimizer.

    Returns:
        Dict[str, Any]: The flattened optimizer state dict.
    """
    SimpleProfiler.reset()

    unflat_osd = optim_state_dict
    if "state" not in unflat_osd and not rank0_only:
        raise ValueError(
            '`optim_state_dict` must have the keys "state"'
            "to be a valid optimizer state dict"
        )
    param_to_fqns = _get_param_to_fqns(model)
    fqn_to_fsdp_param_info = _get_fqn_to_fsdp_param_info(model)
    fsdp_state = next(iter(fqn_to_fsdp_param_info.values())).state

    # Broadcast unflat_osd without non-scalar tensor if rank0_only is True.
    if rank0_only:
        unflat_osd = _broadcast_processed_state(fsdp_state, unflat_osd, group=group)

    # Construct the "state" part
    flat_osd_state: dict[_OptimStateKey | str, Any] = {}
    unflat_osd_state = unflat_osd["state"]
    all_state_keys = set(unflat_osd_state.keys())

    for param, fqns in param_to_fqns.items():
        fqn = fqns[0]
        if fqn not in unflat_osd_state:
            continue
        all_state_keys.difference_update(fqns)

        if rank0_only:
            for fqn in fqns:
                if not unflat_osd_state[fqn]:
                    continue
                for state_name in unflat_osd_state[fqn]:
                    unflat_osd_state[fqn][state_name] = _broadcast_state(
                        fsdp_state, unflat_osd_state[fqn][state_name], group=group
                    )
            fqn = fqns[0]
        if fqn in fqn_to_fsdp_param_info:
            fsdp_param_info = fqn_to_fsdp_param_info[fqn]
            if use_orig_params:
                with SimpleProfiler.profile(SimpleProfiler.Type.RESHARDING):
                    flat_state = _shard_orig_param_state(
                        fsdp_param_info,
                        fqn,
                        unflat_osd_state[fqn],
                    )
            else:
                flat_state = _flatten_optim_state(
                    fsdp_param_info,
                    unflat_osd_state,
                    fqns,
                )
            key = _OptimStateKey(tuple(fqns), True)
            # Only include non-empty states since as expected by
            # `torch.optim.Optimizer` s unless the optimizer is KeyedOptimizer
            # or NamedOptimizer.
            if flat_state:
                flat_osd_state[key] = flat_state
            elif use_orig_params:
                if len(fqns) != 1:
                    raise AssertionError(
                        f"use_orig_params is True but there are multiple FQNs, {fqns}."
                    )
                if optim is not None:  # NamedOptimizer or KeyedOptimizer case.
                    state = optim.state.get(param, None)  # type: ignore[call-overload]
                    if state is not None:
                        flat_osd_state[key] = copy.deepcopy(state)
                    else:
                        warnings.warn(
                            f"optim_state[{key}] is not on rank{fsdp_state.rank}.",
                            stacklevel=2,
                        )

            else:
                raise RuntimeError(
                    f"The state of {key} is empty. This should happen when "
                    "use_orig_params=True."
                )
        else:  # do not flatten non-FSDP parameters' states
            if len(fqns) != 1:
                raise AssertionError(f"Expected len(fqns) == 1, got {len(fqns)}")
            key = _OptimStateKey(tuple(fqns), False)
            flat_osd_state[key] = copy.copy(unflat_osd_state[fqn])

        if rank0_only:
            for fqn in fqns:
                if not unflat_osd_state[fqn]:
                    continue
                for state_name, param_state in list(unflat_osd_state[fqn].items()):
                    if fsdp_state.rank > 0:
                        # Deference the tensor so that PyTorch can collect the memory.
                        del unflat_osd_state[fqn][state_name]
                    else:
                        # Move the tensor in the original osd back to CPU to make the
                        # original osd unaffected.
                        unflat_osd_state[fqn][state_name] = param_state.cpu()

    # Handle user-defined state, states that are not associated with parameters.
    for key in all_state_keys:
        user_state = unflat_osd_state[key]
        if isinstance(user_state, torch.Tensor) and rank0_only and use_orig_params:
            user_state = _broadcast_state(fsdp_state, user_state, group=group)
        flat_osd_state[key] = copy.copy(user_state)

    SimpleProfiler.dump_and_reset("FSDP _flatten_optim_state_dict() profiling: ")
    # Construct the "param_groups" part -- copy as is since it will be
    # rekeyed later according to the target rank's optimizer
    # Only copy param_groups if it exists in unflat_osd
    if "param_groups" in unflat_osd:
        flat_osd_param_groups = copy.deepcopy(unflat_osd["param_groups"])
        return {"state": flat_osd_state, "param_groups": flat_osd_param_groups}
    else:
        return {"state": flat_osd_state}

