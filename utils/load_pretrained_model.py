
def load_pretrained_model(model_name, config, cache_dir, custom_model_class, is_tf_model=False):
    model_class_name = modelclass_dispatcher(model_name, custom_model_class)

    if model_class_name == "GPT2ModelNoPastState":
        if is_tf_model:
            return TFGPT2ModelNoPastState.from_pretrained(model_name, config=config, cache_dir=cache_dir)
        else:
            return GPT2ModelNoPastState.from_pretrained(model_name, config=config, cache_dir=cache_dir)

    if is_tf_model:
        model_class_name = "TF" + model_class_name

    transformers_module = __import__("transformers", fromlist=[model_class_name])
    logger.info(f"Model class name: {model_class_name}")
    model_class = getattr(transformers_module, model_class_name)

    return model_class.from_pretrained(model_name, config=config, cache_dir=cache_dir)

