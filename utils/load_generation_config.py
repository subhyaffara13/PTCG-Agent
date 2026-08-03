import os

def load_generation_config(generation_config: str | None) -> GenerationConfig:
    if generation_config is None:
        return GenerationConfig()

    if ".json" in generation_config:  # is a local file
        dirname = os.path.dirname(generation_config)
        filename = os.path.basename(generation_config)
        return GenerationConfig.from_pretrained(dirname, filename)
    else:
        return GenerationConfig.from_pretrained(generation_config)

