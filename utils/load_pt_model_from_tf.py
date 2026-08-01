
def load_pt_model_from_tf(model_name):
    # Note that we could get pt model from tf, but model source and its structure in this case is different from directly using
    # load_pt_model() and load_tf_model() even with the same name. Therefore it should not be used for comparing with them
    from convert_tf_models_to_pytorch import tf2pt_pipeline  # noqa: PLC0415

    config, model = tf2pt_pipeline(model_name)

    return config, model

