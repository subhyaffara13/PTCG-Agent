
def tf2pt_pipeline(model_name, is_tf2=False):
    if model_name not in TFMODELS:
        raise NotImplementedError(model_name + " not implemented")
    tf_checkpoint_path = download_tf_checkpoint(model_name)
    config, init_model = init_pytorch_model(model_name, tf_checkpoint_path)
    model = convert_tf_checkpoint_to_pytorch(model_name, config, init_model, tf_checkpoint_path, is_tf2)
    # Could then use the model in Benchmark
    return config, model

