
def get_qconv2d_binary_pt2e_pattern(x_scale_zp_are_tensors=False, users=1):
    qconv_op = (
        torch.ops.onednn.qconv2d_pointwise.binary_tensor
        if x_scale_zp_are_tensors
        else torch.ops.onednn.qconv2d_pointwise.binary
    )
    return CallFunction(
        qconv_op,
        KeywordArg("x"),
        KeywordArg("x_scale"),
        KeywordArg("x_zp"),
        KeywordArg("packed_weight"),
        KeywordArg("w_scale"),
        KeywordArg("w_zp"),
        KeywordArg("accum"),
        KeywordArg("b"),
        KeywordArg("stride"),
        KeywordArg("padding"),
        KeywordArg("dilation"),
        KeywordArg("groups"),
        KeywordArg("output_scale"),
        KeywordArg("output_zero_point"),
        KeywordArg("output_dtype"),
        KeywordArg("accum_scale"),
        KeywordArg("accum_zero_point"),
        KeywordArg("binary_op_name"),
        KeywordArg("alpha"),
        KeywordArg("unary_op_name"),
        KeywordArg("unary_op_args"),
        KeywordArg("unary_op_algorithm"),
        _users=users,
    )

