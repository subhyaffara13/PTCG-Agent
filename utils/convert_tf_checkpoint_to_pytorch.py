
def convert_tf_checkpoint_to_pytorch(model_name, config, init_model, tf_checkpoint_path, is_tf2):
    load_tf_weight_func_name = "load_tf_weights_in_" + TFMODELS[model_name][0]

    module = __import__("transformers", fromlist=[load_tf_weight_func_name])

    if is_tf2 is False:
        load_tf_weight_func = getattr(module, load_tf_weight_func_name)
    else:
        if TFMODELS[model_name][0] != "bert":
            raise NotImplementedError("Only support tf2 ckeckpoint for Bert model")
        from transformers import convert_bert_original_tf2_checkpoint_to_pytorch  # noqa: PLC0415

        load_tf_weight_func = convert_bert_original_tf2_checkpoint_to_pytorch.load_tf2_weights_in_bert

    # Expect transformers team will unify the order of signature in the future
    model = (
        load_tf_weight_func(init_model, config, tf_checkpoint_path)
        if is_tf2 is False
        else load_tf_weight_func(init_model, tf_checkpoint_path, config)
    )
    model.eval()
    return model

