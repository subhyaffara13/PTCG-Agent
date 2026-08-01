
def mark_step_begin() -> None:
    "Indicates that a new iteration of inference or training is about to begin."

    # iterate down to distinguish from GenerationTracking counter
    MarkStepBox.mark_step_counter -= 1

