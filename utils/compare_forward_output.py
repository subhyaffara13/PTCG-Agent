
def compare_forward_output(pred_base, pred_control, precision):
    return compare_tuple_tensors(
        pred_base,
        pred_control,
        precision,
    )

