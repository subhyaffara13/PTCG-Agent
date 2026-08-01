
def _get_model_list(pipeline_type: str):
    if pipeline_type == "sd3":
        return ["text_encoder", "text_encoder_2", "text_encoder_3", "transformer", "vae_encoder", "vae_decoder"]

    if pipeline_type == "flux":
        return ["text_encoder", "text_encoder_2", "transformer", "vae_encoder", "vae_decoder"]

    if pipeline_type == "sdxl":
        return ["text_encoder", "text_encoder_2", "unet", "vae_encoder", "vae_decoder"]

    assert pipeline_type == "sd"
    return ["text_encoder", "unet", "vae_encoder", "vae_decoder"]

