
def _save_checkpoint(iteration_id, model_path):
    if iteration_id is not None:
        try:
            from factory.model_checkpoint_manager import ModelCheckpointManager
            ModelCheckpointManager().save_checkpoint(model_path, iteration_id)
        except Exception as e:
            logger.warning(f"Failed to save model checkpoint: {e}")

