
def _save_state_dict(
    state_dict: STATE_DICT_TYPE,
    storage_writer: StorageWriter,
    process_group: dist.ProcessGroup | None = None,
    coordinator_rank: int = 0,
    no_dist: bool = False,
    planner: SavePlanner | None = None,
    use_collectives: bool = True,
) -> Metadata:
    torch._C._log_api_usage_once("torch.distributed.checkpoint.save_state_dict")

    distW = _DistWrapper(process_group, not no_dist, coordinator_rank)
    if planner is None:
        planner = DefaultSavePlanner()
    if planner is None:
        raise AssertionError("planner is None")

    global_metadata = None

    ckpt_kwargs = {}
    if (ckpt_id := getattr(storage_writer, "checkpoint_id", None)) is not None:
        ckpt_kwargs["checkpoint_id"] = ckpt_id
        ckpt_kwargs["process_group"] = distW.group

    @_dcp_method_logger(**ckpt_kwargs)
    def local_step():
        if planner is None:
            raise AssertionError("planner is None")
        storage_meta = storage_writer.storage_meta()
        if "storage_meta" not in inspect.signature(planner.set_up_planner).parameters:
            warnings.warn(
                "The function definition for SavePlanner.set_up_planner has been updated"
                " to include the storage_meta argument. Please update your implementation"
                " to include this parameter.",
                stacklevel=2,
            )
            planner.set_up_planner(state_dict, distW.is_coordinator)  # type: ignore[call-arg, arg-type]
        else:
            planner.set_up_planner(
                state_dict=state_dict,
                storage_meta=storage_meta,
                is_coordinator=distW.is_coordinator,
            )

        if (
            "kwargs"
            in inspect.signature(storage_writer.set_up_storage_writer).parameters
        ):
            storage_writer.set_up_storage_writer(
                distW.is_coordinator,
                rank=distW.rank,
                use_collectives=use_collectives,
            )
        else:
            storage_writer.set_up_storage_writer(distW.is_coordinator)

        local_plan = planner.create_local_plan()
        local_plan = storage_writer.prepare_local_plan(local_plan)
        return local_plan

    @_dcp_method_logger(**ckpt_kwargs)
    def global_step(all_local_plans):
        nonlocal global_metadata

        if planner is None:
            raise AssertionError("planner is None")
        all_local_plans, global_metadata = planner.create_global_plan(all_local_plans)
        all_local_plans = storage_writer.prepare_global_plan(all_local_plans)
        return all_local_plans

    central_plan: SavePlan | None = None
    if use_collectives:
        central_plan = distW.reduce_scatter("plan", local_step, global_step)
    else:
        local_plan: SavePlan = local_step()
        global_plan: list[SavePlan] = global_step([local_plan])
        central_plan = global_plan[0]

    @_dcp_method_logger(**ckpt_kwargs)
    def write_data():
        if planner is None:
            raise AssertionError("planner is None")
        if central_plan is None:
            raise AssertionError("central_plan is None")
        final_local_plan = planner.finish_plan(central_plan)
        all_writes = storage_writer.write_data(final_local_plan, planner)

        all_writes.wait()
        return all_writes.value()

    @_dcp_method_logger(**ckpt_kwargs)
    def finish_checkpoint(all_results):
        if global_metadata is None:
            raise AssertionError("global_metadata is None")
        storage_writer.finish(metadata=global_metadata, results=all_results)
        return global_metadata

    if use_collectives:
        metadata = distW.all_reduce("write", write_data, finish_checkpoint)
    else:
        write_results: list[WriteResult] = write_data()
        metadata = finish_checkpoint([write_results])
        distW.barrier()

    return metadata

