import os
from typing import Any

def _load_state_dict(
    archive_reader: PT2ArchiveReader,
    model_name: str,
) -> dict[str, torch.Tensor] | bytes:
    # Make it BC compatible with legacy weight files
    legacy_weights_file = f"{WEIGHTS_DIR}{model_name}.pt"
    if legacy_weights_file in archive_reader.get_file_names():
        logger.warning(
            "You are loading weight from the legacy format. "
            "Please generate a new pt2 file using torch.export.save()."
        )
        return archive_reader.read_bytes(legacy_weights_file)
    else:
        weights_config_file = WEIGHTS_CONFIG_FILENAME_FORMAT.format(model_name)
        if weights_config_file not in archive_reader.get_file_names():
            raise AssertionError(f"{weights_config_file} not found in PT2 archive")
        weights_config = _load_payload_config(archive_reader, weights_config_file)
        # construct the mapping from file name (e.g. weight_0) to flat weight payload
        state_dict_file_map = _build_file_map(
            archive_reader, weights_config, WEIGHTS_DIR
        )
        # chain the mapping weight FQN -> weight file name -> strided weight payload
        # so that the aliasing of weights is preserved
        state_dict: dict[str, torch.Tensor] = {}
        for weight_fqn, payload_meta in weights_config.config.items():
            if payload_meta.use_pickle:
                weight_bytes = archive_reader.read_bytes(
                    os.path.join(WEIGHTS_DIR, payload_meta.path_name)
                )
                state_dict[weight_fqn] = torch.load(
                    io.BytesIO(weight_bytes), weights_only=False
                )
            else:
                tensor_meta = payload_meta.tensor_meta
                if tensor_meta is None:
                    raise AssertionError(
                        "tensor_meta cannot be None for non-pickled weight"
                    )
                weight_tensor = torch.as_strided(
                    input=state_dict_file_map[payload_meta.path_name],
                    size=deserialize_size(tensor_meta.sizes),
                    stride=deserialize_stride(tensor_meta.strides),
                    storage_offset=deserialize_storage_offset(
                        tensor_meta.storage_offset
                    ),
                )
                if payload_meta.is_param:
                    state_dict[weight_fqn] = torch.nn.Parameter(
                        weight_tensor, requires_grad=tensor_meta.requires_grad
                    )
                else:
                    state_dict[weight_fqn] = weight_tensor

        return state_dict


def _load_state_dict(
    state_dict: dict[str, Any],
    storage_reader: StorageReader,
    process_group: dist.ProcessGroup | None = None,
    coordinator_rank: int = 0,
    no_dist: bool = False,
    planner: LoadPlanner | None = None,
) -> None:
    torch._C._log_api_usage_once("torch.distributed.checkpoint.load_state_dict")

    distW = _DistWrapper(process_group, not no_dist, coordinator_rank)
    if planner is None:
        planner = DefaultLoadPlanner()

    ckpt_kwargs = {}
    if (ckpt_id := getattr(storage_reader, "checkpoint_id", None)) is not None:
        ckpt_kwargs["checkpoint_id"] = ckpt_id
        ckpt_kwargs["process_group"] = distW.group

    use_collectives = True
    metadata: Metadata | None = None

    @_dcp_method_logger(**ckpt_kwargs)
    def local_step():
        nonlocal use_collectives
        nonlocal metadata

        # Use global metadata if available, otherwise fallback to rank local metadata
        global_metadata_exc: Exception | None = None
        rank_metadata_exc: Exception | None = None
        try:
            metadata = storage_reader.read_metadata()
        except Exception as e:
            global_metadata_exc = e
            logger.warning(
                "Global metadata is not found. Falling back to rank local metadata.",
                exc_info=True,
            )

        if (
            not metadata
            and "kwargs" in inspect.signature(storage_reader.read_metadata).parameters
        ):
            try:
                metadata = storage_reader.read_metadata(rank=distW.rank)  # noqa: F841
                use_collectives = False
            except Exception as e:
                rank_metadata_exc = e
                logger.warning("Rank local metadata is not found.", exc_info=True)

        if planner is None:
            raise AssertionError("planner is None")
        if metadata is None:
            error_parts = ["metadata is None"]
            if global_metadata_exc is not None:
                error_parts.append(
                    f"global metadata read failed: {global_metadata_exc}"
                )
            if rank_metadata_exc is not None:
                error_parts.append(
                    f"rank local metadata read failed: {rank_metadata_exc}"
                )
            raise AssertionError("; ".join(error_parts))
        planner.set_up_planner(state_dict, metadata, distW.is_coordinator)

        if (
            "kwargs"
            in inspect.signature(storage_reader.set_up_storage_reader).parameters
        ):
            storage_reader.set_up_storage_reader(
                metadata,
                distW.is_coordinator,
                rank=distW.rank,
                use_collectives=use_collectives,
            )
        else:
            storage_reader.set_up_storage_reader(metadata, distW.is_coordinator)

        local_plan = planner.create_local_plan()
        local_plan = storage_reader.prepare_local_plan(local_plan)
        return local_plan

    @_dcp_method_logger(**ckpt_kwargs)
    def global_step(all_local_plans):
        if planner is None:
            raise AssertionError("planner is None")
        all_local_plans = planner.create_global_plan(all_local_plans)
        all_local_plans = storage_reader.prepare_global_plan(all_local_plans)
        return all_local_plans

    central_plan: LoadPlan | None = None
    if use_collectives:
        central_plan = distW.reduce_scatter("plan", local_step, global_step)
    else:
        local_plan: LoadPlan = local_step()
        global_plan: list[LoadPlan] = global_step([local_plan])
        central_plan = global_plan[0]

    @_dcp_method_logger(**ckpt_kwargs)
    def read_data():
        if planner is None:
            raise AssertionError("planner is None")
        if central_plan is None:
            raise AssertionError("central_plan is None")
        final_local_plan = planner.finish_plan(central_plan)
        all_reads = storage_reader.read_data(final_local_plan, planner)

        all_reads.wait()
        return None

    if use_collectives:
        _ = distW.all_gather("read", read_data)
    else:
        read_data()
        distW.barrier()

