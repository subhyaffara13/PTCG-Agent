
def get_image_filename_prefix(engine: str, model_name: str, batch_size: int, steps: int, disable_safety_checker: bool):
    short_model_name = model_name.split("/")[-1].replace("stable-diffusion-", "sd")
    return f"{engine}_{short_model_name}_b{batch_size}_s{steps}" + ("" if disable_safety_checker else "_safe")

