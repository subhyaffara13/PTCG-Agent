
def skip_frame_if_in_functorch_mode(val: torch.Tensor) -> None:
    try:
        val.data_ptr()  # will throw for functorch tensors
    except RuntimeError as e:
        from .exc import unimplemented

        # This will be GradTrackingTensor/BatchedTensor/etc
        functorch_subclass_name = re.sub(r"\(.*", "", repr(val))

        unimplemented(
            gb_type="skip frame due to being in functorh mode",
            context="",
            explanation=f"torch.compile cannot be run in context: {functorch_subclass_name}. Skipping frame.",
            hints=[],
            from_exc=e,
            skip_frame=True,
        )

