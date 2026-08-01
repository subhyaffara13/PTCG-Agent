
def compare_parameters(model_base, model_control, precision):
    return compare_dict_tensors(
        dict(model_base.named_parameters()),
        dict(model_control.named_parameters()),
        precision,
    )

