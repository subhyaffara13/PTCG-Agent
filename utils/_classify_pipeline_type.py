from pathlib import Path


def _classify_pipeline_type(source_dir: Path):
    # May also check _class_name in model_index.json like `StableDiffusion3Pipeline` or `FluxPipeline` etc to classify.
    if is_sd_3(source_dir):
        return "sd3"

    if is_flux(source_dir):
        return "flux"

    if is_sdxl(source_dir):
        return "sdxl"

    # sd 1.x and 2.x
    return "sd"

