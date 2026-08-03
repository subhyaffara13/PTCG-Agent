import copy

def deepspeed_optim_sched(trainer, hf_deepspeed_config, args, num_training_steps, model_parameters):
    """
    A convenience wrapper that deals with optimizer and lr scheduler configuration.
    """
    from accelerate.utils import DummyOptim, DummyScheduler

    config = hf_deepspeed_config.config

    # Mixing and matching DS schedulers and optimizers is supported unless Offload is enabled in which case it's:
    # 1. DS scheduler + DS optimizer: Yes
    # 2. HF scheduler + HF optimizer: Mostly*
    # 3. DS scheduler + HF optimizer: Mostly*
    # 4. HF scheduler + DS optimizer: Yes
    #
    # Mostly*: All non-native DeepSpeed optimizers that have both CPU and GPU implementation should work (except LAMB)

    optimizer = None
    if "optimizer" in config:
        optimizer = DummyOptim(params=model_parameters)
    else:
        if hf_deepspeed_config.is_offload():
            logger.info(
                "Detected ZeRO Offload and non-DeepSpeed optimizers: This combination should work as long as the"
                " custom optimizer has both CPU and GPU implementation (except LAMB)"
            )

        # ds supports Adam, OneBitAdam, and Lamb optimizers and can import other optimizers from torch.
        # But trainer uses AdamW by default.
        optimizer = trainer.create_optimizer()
        # To use other optimizers requires voiding warranty with: `zero_allow_untested_optimizer`
        config["zero_allow_untested_optimizer"] = True

    lr_scheduler = None
    if "scheduler" in config:
        lr_scheduler = DummyScheduler(optimizer)
    else:
        if isinstance(optimizer, DummyOptim):

            def _lr_scheduler_callable(optimizer):
                # create a shallow copy first, so later modifications do not affect original trainer
                trainer_copy = copy.copy(trainer)
                # at the time _lr_scheduler_callable is called, trainer.lr_scheduler has been set
                # update it to None so that we can re-create a new scheduler
                trainer_copy.lr_scheduler = None
                lr_scheduler = trainer_copy.create_scheduler(
                    num_training_steps=num_training_steps, optimizer=optimizer
                )
                return lr_scheduler

            lr_scheduler = DummyScheduler(optimizer, lr_scheduler_callable=_lr_scheduler_callable)

    return optimizer, lr_scheduler

