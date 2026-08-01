
def create_functionalized_rng_ops_wrapper(
    func: Callable[..., Any],
    args: Any,
    args_descs: list[AOTInput],
    trace_joint: bool = True,
) -> Any:
    # Functionalization of rng ops changes the calling convention of the joint graph.
    # It goes from (primals, tangents) to (seed, offset, primals, tangents)
    # At runtime, we pass on the current seed and offset. This is hidden from
    # the user.
    fake_mode_det = detect_fake_mode()
    fake_mode: AbstractContextManager[Any] = nullcontext()
    if fake_mode_det is not None:
        fake_mode = fake_mode_det

    def override_get_rng_state(
        device: int | str | torch.device = "cuda",
    ) -> Tensor:
        out = PhiloxStateTracker.get_state_as_tensor()
        return out

    def override_set_rng_state(
        x: Tensor, device: int | str | torch.device = "cuda"
    ) -> None:
        PhiloxStateTracker.set_state_from_tensor(x)

    def append_rng_offsets(outs: Any, outs_descs: Any) -> Any:
        if trace_joint:
            # outs signature before: Tuple(fwd_outputs), Tuple(bwd_outputs)
            # outs signature after: Tuple(fwd_outputs, new_fwd_rng_offset), Tuple(bwd_offset, new_bwd_rng_offset)
            return (
                (
                    (*outs[0], PhiloxStateTracker.get_updated_fwd_offset()),
                    (*outs[1], PhiloxStateTracker.get_updated_bwd_offset()),
                ),
                (
                    (*outs_descs[0], PhiloxUpdatedForwardOffsetAOTOutput()),
                    (*outs_descs[1], PhiloxUpdatedBackwardOffsetAOTOutput()),
                ),
            )
        else:
            # outs signature before: Tuple(fwd_outputs)
            # outs signature after: Tuple(fwd_outputs, new_fwd_rng_offset)
            return (
                (*outs, PhiloxStateTracker.get_updated_fwd_offset()),
                (*outs_descs, PhiloxUpdatedForwardOffsetAOTOutput()),
            )

    def traced_joint(
        primals: list[FxValue],
        tangents: list[FxValue],
        fwd_seed: Tensor,
        fwd_base_offset: Tensor,
        bwd_seed: Tensor,
        bwd_base_offset: Tensor,
    ) -> tuple[
        tuple[tuple[FxValue, ...], tuple[FxValue, ...]],
        tuple[tuple[AOTOutput, ...], tuple[AOTOutput, ...]],
    ]:
        with (
            patch("torch.cuda.get_rng_state", override_get_rng_state),
            patch("torch.cuda.set_rng_state", override_set_rng_state),
        ):
            return append_rng_offsets(*func(primals, tangents))

    def traced_forward(*primals_fwd_seed_fwd_base_offset: Any) -> Any:
        # The signature is (*primals, seed, offset)
        with (
            patch("torch.cuda.get_rng_state", override_get_rng_state),
            patch("torch.cuda.set_rng_state", override_set_rng_state),
        ):
            return append_rng_offsets(*func(*primals_fwd_seed_fwd_base_offset[:-2]))

    if trace_joint:
        # Get the current seed and offset to setup tracing.
        fwd_seed, fwd_base_offset = CUDARngStateHelper.get_torch_state_as_tuple(
            fake_mode
        )
        bwd_seed, bwd_base_offset = CUDARngStateHelper.get_torch_state_as_tuple(
            fake_mode
        )
        PhiloxStateTracker.record_state(fwd_seed, fwd_base_offset, "forward")
        PhiloxStateTracker.record_state(bwd_seed, bwd_base_offset, "backward")
        return (
            traced_joint,
            (
                *args,
                fwd_seed,
                fwd_base_offset,
                bwd_seed,
                bwd_base_offset,
            ),
            (
                *args_descs,
                PhiloxForwardSeedAOTInput(),
                PhiloxForwardBaseOffsetAOTInput(),
                PhiloxBackwardSeedAOTInput(),
                PhiloxBackwardBaseOffsetAOTInput(),
            ),
        )
    else:
        # Get the current seed and offset to setup tracing.
        fwd_seed, fwd_base_offset = CUDARngStateHelper.get_torch_state_as_tuple(
            fake_mode
        )
        PhiloxStateTracker.record_state(fwd_seed, fwd_base_offset, "forward")
        return (
            traced_forward,
            (*args, fwd_seed, fwd_base_offset),
            (
                *args_descs,
                PhiloxForwardSeedAOTInput(),
                PhiloxForwardBaseOffsetAOTInput(),
            ),
        )

