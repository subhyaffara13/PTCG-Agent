
def check_memory_step(
    allocated: list[str], freed: list[str], is_final_step: bool = False
) -> None:
    tracker = get_mem_tracker()
    tracker.check_step_delta(allocated, freed, is_final_step)

