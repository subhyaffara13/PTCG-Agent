
def init_pytorch_model(model_name, tf_checkpoint_path):
    config_name = TFMODELS[model_name][1]
    config_module = __import__("transformers", fromlist=[config_name])
    model_config = getattr(config_module, config_name)

    parent_path = tf_checkpoint_path.rpartition("/")[0]
    config_path = glob.glob(parent_path + "/*config.json")
    config = model_config() if len(config_path) == 0 else model_config.from_json_file(str(config_path[0]))

    if not TFMODELS[model_name][2]:
        from transformers import AutoModelForPreTraining  # noqa: PLC0415

        init_model = AutoModelForPreTraining.from_config(config)
    else:
        model_categroy_name = TFMODELS[model_name][2]
        module = __import__("transformers", fromlist=[model_categroy_name])
        model_categroy = getattr(module, model_categroy_name)
        init_model = model_categroy(config)
    return config, init_model

