
def load_non_ext_class(
    builder: IRBuilder, ir: ClassIR, non_ext: NonExtClassInfo, line: int
) -> Value:
    cls_name = builder.load_str(ir.name)

    add_dunders_to_non_ext_dict(builder, non_ext, line)

    class_type_obj = builder.py_call(
        non_ext.metaclass, [cls_name, non_ext.bases, non_ext.dict], line
    )
    return class_type_obj

