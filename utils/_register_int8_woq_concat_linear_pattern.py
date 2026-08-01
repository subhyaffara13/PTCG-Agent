
def _register_int8_woq_concat_linear_pattern():
    def _create_wgt_node(wgt_node_name: str):
        return CallFunction(
            prims.convert_element_type.default,
            CallFunction(
                aten.permute.default,
                KeywordArg(wgt_node_name),
                Arg(),
            ),
            Arg(),
        )

    cat_wgt = CallFunction(
        aten.cat.default, [_create_wgt_node(wgt) for wgt in ["w1", "w2", "w3"]], 1
    )

    _woq_pattern = CallFunction(
        aten.mul.Tensor,
        CallFunction(aten.mm.default, KeywordArg("x"), cat_wgt),
        KeywordArg("scales"),
    )
    _register_concat_linear_int8_woq_lowering(
        _woq_pattern, aten._weight_int8pack_mm.default, aten.reshape
    )

