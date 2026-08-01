
def load_tf_model(model_name, model_class, cache_dir, config_modifier):
    config = AutoConfig.from_pretrained(model_name, cache_dir=cache_dir)

    config_modifier.modify(config)
    # Loading tf model from transformers limits the cpu affinity to {0} when KMP_AFFINITY is set
    # Restore the affinity after model loading for expected ORT performance
    affinity_setting = AffinitySetting()
    affinity_setting.get_affinity()
    model = load_pretrained_model(
        model_name,
        config=config,
        cache_dir=cache_dir,
        custom_model_class=model_class,
        is_tf_model=True,
    )
    affinity_setting.set_affinity()

    return config, model

