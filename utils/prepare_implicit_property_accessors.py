
def prepare_implicit_property_accessors(
    info: TypeInfo, ir: ClassIR, module_name: str, mapper: Mapper
) -> None:
    concrete_attributes = set()
    for base in ir.base_mro:
        for name, attr_rtype in base.attributes.items():
            concrete_attributes.add(name)
            add_property_methods_for_attribute_if_needed(
                info, ir, name, attr_rtype, module_name, mapper
            )
    for base in ir.mro[1:]:
        if base.is_trait:
            for name, attr_rtype in base.attributes.items():
                if name not in concrete_attributes:
                    add_property_methods_for_attribute_if_needed(
                        info, ir, name, attr_rtype, module_name, mapper
                    )

