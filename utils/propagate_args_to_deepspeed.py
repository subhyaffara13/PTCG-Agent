
def propagate_args_to_deepspeed(accelerator, args, auto_find_batch_size=False):
    """
    Sets values in the deepspeed plugin based on the TrainingArguments.

    Args:
        accelerator (`Accelerator`): The Accelerator object.
        args (`TrainingArguments`): The training arguments to propagate to DeepSpeed config.
        auto_find_batch_size (`bool`, *optional*, defaults to `False`):
            Whether batch size was auto-discovered by trying increasingly smaller sizes.
    """
    ds_plugin = accelerator.state.deepspeed_plugin

    ds_plugin.hf_ds_config = HfTrainerDeepSpeedConfig(ds_plugin.hf_ds_config.config)
    ds_plugin.deepspeed_config = ds_plugin.hf_ds_config.config
    ds_plugin.hf_ds_config.trainer_config_process(args, auto_find_batch_size)

