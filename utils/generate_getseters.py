
def generate_getseters(cl: ClassIR, emitter: Emitter) -> None:
    if not cl.is_trait:
        for i, (attr, rtype) in enumerate(cl.attributes.items()):
            generate_getter(cl, attr, rtype, emitter)
            # Final attributes are read-only, so they have no setter.
            if attr not in cl.final_attributes:
                emitter.emit_line("")
                generate_setter(cl, attr, rtype, emitter)
            if i < len(cl.attributes) - 1:
                emitter.emit_line("")
    for prop, (getter, setter) in cl.properties.items():
        if getter.decl.implicit:
            continue

        rtype = getter.sig.ret_type
        emitter.emit_line("")
        generate_readonly_getter(cl, prop, rtype, getter, emitter)
        if setter:
            arg_type = setter.sig.args[1].type
            emitter.emit_line("")
            generate_property_setter(cl, prop, arg_type, setter, emitter)

