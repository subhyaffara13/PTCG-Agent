
def _optimizer_post_hook(
    optimizer: Optimizer, args: tuple[Unpack[_Ts]], kwargs: dict[str, Any]
) -> None:
    KinetoStepTracker.increment_step("Optimizer")

