
def _register_woq_mm_int8_pattern4():
    _woq_pattern = CallFunction(
        aten.mul.Tensor,
        CallFunction(
            aten.mm.default,
            KeywordArg("x"),
            CallFunction(
                prims.convert_element_type.default,
                CallFunction(
                    aten.permute.default,
                    KeywordArg("weight"),
                    Arg(),
                ),
                Arg(),
            ),
        ),
        KeywordArg("scales"),
    )
    _register_woq_lowering(_woq_pattern, aten._weight_int8pack_mm.default, aten.reshape)

