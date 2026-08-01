
def setup_generator_class(builder: IRBuilder) -> ClassIR:
    mapper = builder.mapper
    assert isinstance(builder.fn_info.fitem, FuncDef), builder.fn_info.fitem
    generator_class_ir = mapper.fdef_to_generator[builder.fn_info.fitem]
    if builder.fn_info.can_merge_generator_and_env_classes():
        builder.fn_info.env_class = generator_class_ir
    else:
        generator_class_ir.attributes[ENV_ATTR_NAME] = RInstance(builder.fn_info.env_class)

    builder.classes.append(generator_class_ir)
    return generator_class_ir

