
def _get_cosine_with_min_lr_schedule_with_warmup_lr_rate_lambda(
    current_step: int,
    *,
    num_warmup_steps: int,
    num_training_steps: int,
    num_cycles: float,
    min_lr_rate: float = 0.0,
    warmup_lr_rate: float | None = None,
):
    current_step = float(current_step)
    num_warmup_steps = float(num_warmup_steps)
    num_training_steps = float(num_training_steps)

    if current_step < num_warmup_steps:
        if warmup_lr_rate is None:
            return (current_step + 1.0) / max(1.0, num_warmup_steps)
        else:
            warmup_lr_rate = float(warmup_lr_rate)
            return warmup_lr_rate + (1.0 - warmup_lr_rate) * (current_step) / (max(1, num_warmup_steps - 1))
    progress = (current_step - num_warmup_steps + 1.0) / (max(1.0, num_training_steps - num_warmup_steps))
    factor = 0.5 * (1.0 + math.cos(math.pi * num_cycles * 2.0 * progress))
    factor = factor * (1 - min_lr_rate) + min_lr_rate
    return max(0, factor)

