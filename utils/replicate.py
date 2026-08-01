
def replicate(tree, devices=None, axis_name='_device_put_sharded'):
  """Replicates arrays to multiple devices.

  Args:
    tree: a pytree containing the arrays that should be replicated.
    devices: the devices the data is replicated to
      (default: same order as expected by ``jax.pmap()``).
    axis_name: the axis name to use for the replication.
  Returns:
    A new pytree containing the replicated arrays.
  """
  devices = devices or _pmap_device_order()
  mesh = jax.sharding.Mesh(np.array(devices), (axis_name,))
  sharding = jax.NamedSharding(mesh, jax.P(axis_name))

  def _replicate(x):
    if isinstance(x, jax.Array):
      return jax.device_put(jnp.stack([x] * len(devices)), sharding)
    return jax.device_put(np.stack([x] * len(devices)), sharding)

  return jax.tree_util.tree_map(_replicate, tree)


def replicate(
    network: T,
    devices: Sequence[int | torch.device],
    detach: bool = False,
) -> list[T]:
    if not _replicatable_module(network):
        raise RuntimeError(
            "Cannot replicate network where python modules are children of ScriptModule"
        )

    if not devices:
        return []

    devices = [_get_device_index(x, True) for x in devices]
    num_replicas = len(devices)

    params = list(network.parameters())
    param_indices = {param: idx for idx, param in enumerate(params)}
    param_copies = _broadcast_coalesced_reshape(params, devices, detach)

    buffers = list(network.buffers())
    buffers_rg: list[torch.Tensor] = []
    buffers_not_rg: list[torch.Tensor] = []
    for buf in buffers:
        if buf.requires_grad and not detach:
            buffers_rg.append(buf)
        else:
            buffers_not_rg.append(buf)

    buffer_indices_rg = {buf: idx for idx, buf in enumerate(buffers_rg)}
    buffer_indices_not_rg = {buf: idx for idx, buf in enumerate(buffers_not_rg)}

    buffer_copies_rg = _broadcast_coalesced_reshape(buffers_rg, devices, detach=detach)
    buffer_copies_not_rg = _broadcast_coalesced_reshape(
        buffers_not_rg, devices, detach=True
    )

    modules = list(network.modules())
    module_copies: list[list[Module]] = [[] for _ in devices]
    module_indices: dict[Module, int] = {}

    for i, module in enumerate(modules):
        module_indices[module] = i
        for j in range(num_replicas):
            replica = module._replicate_for_data_parallel()
            # This is a temporary fix for DDP. DDP needs to access the
            # replicated model parameters. It used to do so through
            # `mode.parameters()`. The fix added in #33907 for DP stops the
            # `parameters()` API from exposing the replicated parameters.
            # Hence, we add a `_former_parameters` dict here to support DDP.
            replica._former_parameters = OrderedDict()

            module_copies[j].append(replica)

    for i, module in enumerate(modules):
        for key, child in module._modules.items():
            if child is None:
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    replica._modules[key] = None
            else:
                module_idx = module_indices[child]
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    setattr(replica, key, module_copies[j][module_idx])
        for key, param in module._parameters.items():
            if param is None:
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    replica._parameters[key] = None
            else:
                param_idx = param_indices[param]
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    param_copy = param_copies[j][param_idx]
                    # parameters in replicas are no longer leaves,
                    # so setattr them as non-parameter attributes
                    setattr(replica, key, param_copy)
                    # expose the parameter for DDP
                    replica._former_parameters[key] = param_copy  # type: ignore[operator, index]
        for key, buf in module._buffers.items():  # type: ignore[assignment]
            if buf is None:
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    replica._buffers[key] = None
            else:
                if buf.requires_grad and not detach:
                    buffer_copies = buffer_copies_rg
                    buffer_idx = buffer_indices_rg[buf]
                else:
                    buffer_copies = buffer_copies_not_rg
                    buffer_idx = buffer_indices_not_rg[buf]
                for j in range(num_replicas):
                    replica = module_copies[j][i]
                    setattr(replica, key, buffer_copies[j][buffer_idx])

    return [cast(T, module_copies[j][0]) for j in range(num_replicas)]


def replicate(
    module: nn.Module,
    ignored_modules: Iterable[torch.nn.Module] | None = None,
    **kwargs,
) -> nn.Module:
    r"""Replicates a module

    Args:
        module (torch.nn.Module): module to replicate

    Example::
        >>> # xdoctest: +REQUIRES(module:torch._C._distributed_c10d)
        >>> module = nn.Linear(3, 3)
        >>> replicate(module)
    """
    torch._C._log_api_usage_once("torch.distributed.replicate")

    # TODO(fegin): using kwargs is not a good idea if we would like to make
    # replicate a formal API to replace DDP.
    if "device_id" in kwargs:
        if not isinstance(kwargs["device_id"], (int, torch.device)):
            raise RuntimeError(
                "Expected device_id to be int or torch.device, "
                f"but got {type(kwargs['device_id'])}"
            )

    if _is_fully_sharded(module):
        raise RuntimeError(
            "Cannot apply `replicate()` on a Module already managed by `fully_shard`"
        )

    if ignored_modules is None:
        ignored_modules = {}
    else:
        ignored_modules = set(ignored_modules)

    state = replicate.state(module)
    module.register_forward_pre_hook(state.forward_pre_hook, with_kwargs=True)
    device_mesh = kwargs.get("device_mesh")
    if device_mesh is not None:
        root_mesh = device_mesh._get_root_mesh()
        # if a root mesh is not the same as device_mesh,
        # meaning the device_mesh is sliced out from the root mesh.
        if root_mesh != device_mesh:
            # TODO: This is a temporary work around to enable DDP + TP.
            # We should do the logic in DDP so that the 2D implementation is
            # sound and the state_dict works out of the box.
            #
            # This won't conflict with what is done in DDP class as the module
            # replicate is going to pass is NOT the original module.
            from torch.distributed.tensor.parallel.ddp import (
                _localize_dtensor,
                _reconstruct_dtensor,
            )

            module.register_forward_pre_hook(_reconstruct_dtensor)
            module.register_forward_hook(_localize_dtensor)

    module.register_forward_hook(state.forward_post_hook)  # type: ignore[arg-type]

    state.record_init_args(module, ignored_modules, **kwargs)

    # Place DDP leftmost for highest priority in the method resolution order
    cls = module.__class__
    dct = {"__deepcopy__": unimplemented_deepcopy}
    new_cls = type(f"DDP{cls.__name__}", (DDP, cls), dct)
    module.__class__ = new_cls
    return module


def replicate(
    module: nn.Module,
    *,
    mesh: DeviceMesh | None = ...,
    mp_policy: MixedPrecisionPolicy = ...,
    offload_policy: OffloadPolicy = ...,
    ignored_params: set[nn.Parameter] | None = ...,
    dp_mesh_dims: DataParallelMeshDims | None = ...,
) -> ReplicateModule: ...


def replicate(
    module: list[nn.Module],
    *,
    mesh: DeviceMesh | None = ...,
    mp_policy: MixedPrecisionPolicy = ...,
    offload_policy: OffloadPolicy = ...,
    ignored_params: set[nn.Parameter] | None = ...,
    dp_mesh_dims: DataParallelMeshDims | None = ...,
) -> list[ReplicateModule]: ...


def replicate(
    module: nn.Module,
    *,
    mesh: DeviceMesh | None = None,
    mp_policy: MixedPrecisionPolicy = MixedPrecisionPolicy(),
    offload_policy: OffloadPolicy = OffloadPolicy(),
    ignored_params: set[nn.Parameter] | None = None,
    dp_mesh_dims: DataParallelMeshDims | None = None,
):
    r"""Replicates a module

    Args:
        module (torch.nn.Module): module to replicate

    Example::
        >>> # xdoctest: +REQUIRES(module:torch._C._distributed_c10d)
        >>> module = nn.Linear(3, 3)
        >>> replicate(module)
    """
    torch._C._log_api_usage_once("torch.distributed._composable.replicate_with_fsdp")
    _validate_module(module)
    mesh = mesh or _init_default_mesh(mesh_dim_names=("replicate",))
    if dp_mesh_dims is not None:
        _validate_mesh_common(mesh, dp_mesh_dims)
        mesh_info = _get_mesh_info(mesh, dp_mesh_dims)
        if not isinstance(mesh_info, DDPMeshInfo):
            raise ValueError(
                "replicate() with dp_mesh_dims requires replicate-only "
                "dims (no shard dims). Use fully_shard() for sharding."
            )
    else:
        _validate_mesh(mesh)
        mesh_info = DDPMeshInfo(mesh, replicate_mesh_dim=0)
    device = _get_device_from_mesh(mesh)
    # managed_modules (3rd return) and buffers (5th return) are unused:
    # - managed_modules: FSDP uses this to set Dynamo-specific attributes
    #   (_is_fsdp_managed_module, _fsdp_use_orig_params), which replicate doesn't need
    # - buffers: already moved to device by _get_modules_and_states; replicate
    #   doesn't need to track them separately
    arg_module, modules, _, params, _ = _get_modules_and_states(
        module,
        device,
        ignored_params,
        is_composable_fn=is_composable_with_replicate,
        get_state_fn=_get_module_replicate_state,
    )
    state = replicate.state(modules[0])  # type: ignore[attr-defined]
    state.init(modules, device, mp_policy)

    _init_param_group(
        state,
        params,
        modules,
        mesh_info,
        None,  # post_forward_mesh_info
        device,
        None,  # shard_placement_fn
        mp_policy,
        offload_policy,
    )

    # Place Replicate leftmost for highest priority in the method resolution order
    _apply_to_module(
        modules,
        cls_to_replicate_cls,
        ReplicateModule,
        "Replicate",
        _unimplemented_deepcopy,
    )
    return arg_module

