
def get_qconv_pt2e_pattern(x_scale_zp_are_tensors=False, users=1):
    qconv_op = (
        torch.ops.onednn.qconv_pointwise.tensor
        if x_scale_zp_are_tensors
        else torch.ops.onednn.qconv_pointwise.default
    )
    return CallFunction(
        qconv_op,
        KeywordArg("x"),
        KeywordArg("x_scale"),
        KeywordArg("x_zp"),
        KeywordArg("packed_weight"),
        KeywordArg("w_scale"),
        KeywordArg("w_zp"),
        KeywordArg("b"),
        KeywordArg("stride"),
        KeywordArg("padding"),
        KeywordArg("dilation"),
        KeywordArg("groups"),
        KeywordArg("output_scale"),
        KeywordArg("output_zero_point"),
        KeywordArg("output_dtype"),
        KeywordArg("postop_name"),
        KeywordArg("postop_args"),
        KeywordArg("postop_algorithm"),
        _users=users,
    )

