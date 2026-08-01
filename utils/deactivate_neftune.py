
def deactivate_neftune(model, hook_handle, accelerator=None):
    """
    Deactivates NEFTune on the model.

    Args:
        model (`torch.nn.Module`):
            The model to deactivate NEFTune on.
        hook_handle (`torch.utils.hooks.RemovableHandle`):
            The hook handle returned by `activate_neftune`.
        accelerator (`Accelerator`, *optional*):
            The accelerator instance. If provided, the model will be unwrapped before
            accessing embeddings.
    """
    if accelerator is not None:
        unwrapped_model = accelerator.unwrap_model(model)
    else:
        unwrapped_model = model

    if _is_peft_model(unwrapped_model):
        embeddings = unwrapped_model.base_model.model.get_input_embeddings()
    else:
        embeddings = unwrapped_model.get_input_embeddings()

    hook_handle.remove()
    if hasattr(embeddings, "neftune_noise_alpha"):
        del embeddings.neftune_noise_alpha

