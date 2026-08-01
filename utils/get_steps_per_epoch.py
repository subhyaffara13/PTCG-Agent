
def get_steps_per_epoch(trainer: Trainer) -> int:
    training_args = trainer.args
    train_dataloader = trainer.get_train_dataloader()

    initial_training_values = trainer.set_initial_training_values(args=training_args, dataloader=train_dataloader)
    steps_per_epoch = initial_training_values[5]

    return steps_per_epoch

