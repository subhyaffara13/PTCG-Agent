
def compare_trainer_and_checkpoint_args(training_args, trainer_state):
    """
    Compare training arguments with those stored in a checkpoint's trainer state.

    Logs a warning if there are mismatches between the current training arguments
    and the ones saved in the checkpoint.

    Args:
        training_args: The current training arguments.
        trainer_state: The trainer state loaded from a checkpoint.
    """
    attributes_map = {
        "logging_steps": "logging_steps",
        "eval_steps": "eval_steps",
        "save_steps": "save_steps",
    }

    has_warning = False
    warning_str = "Warning: The following arguments do not match the ones in the `trainer_state.json` within the checkpoint directory: "
    for arg_attr, state_attr in attributes_map.items():
        arg_value = getattr(training_args, arg_attr, None)
        state_value = getattr(trainer_state, state_attr, None)

        if arg_value is not None and state_value is not None and arg_value != state_value:
            warning_str += f"\n\t{arg_attr}: {arg_value} (from args) != {state_value} (from trainer_state.json)"
            has_warning = True

    # train bs is special as we need to account for multi-GPU
    train_bs_args = training_args.per_device_train_batch_size
    train_bs_state = trainer_state.train_batch_size // max(1, training_args.n_gpu)

    if train_bs_args != train_bs_state:
        warning_str += f"\n\tper_device_train_batch_size: {train_bs_args} (from args) != {train_bs_state} (from trainer_state.json)"
        has_warning = True

    if has_warning:
        logger.warning_once(warning_str)

