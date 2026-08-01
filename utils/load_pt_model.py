
def load_pt_model(model_name, model_class, cache_dir, config_modifier):
    config = AutoConfig.from_pretrained(model_name, cache_dir=cache_dir)
    if hasattr(config, "return_dict"):
        config.return_dict = False

    config_modifier.modify(config)

    model = load_pretrained_model(model_name, config=config, cache_dir=cache_dir, custom_model_class=model_class)

    return config, model

