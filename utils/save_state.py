
def save_state(self):
    """
    Saves the Trainer state, since Trainer.save_model saves only the tokenizer with the model.

    Under distributed environment this is done only for a process with rank 0.
    """
    if not self.is_world_process_zero():
        return

    path = os.path.join(self.args.output_dir, "trainer_state.json")
    self.state.save_to_json(path)

