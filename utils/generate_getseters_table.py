
def generate_getseters_table(cl: ClassIR, name: str, emitter: Emitter) -> None:
    emitter.emit_line(f"static PyGetSetDef {name}[] = {{")
    if not cl.is_trait:
        for attr in cl.attributes:
            emitter.emit_line(f'{{"{attr}",')
            if attr in cl.final_attributes:
                # Final attributes are read-only, so emit a NULL setter.
                emitter.emit_line(f" (getter){getter_name(cl, attr, emitter.names)}, NULL,")
            else:
                emitter.emit_line(
                    " (getter){}, (setter){},".format(
                        getter_name(cl, attr, emitter.names), setter_name(cl, attr, emitter.names)
                    )
                )
            emitter.emit_line(" NULL, NULL},")
    for prop, (getter, setter) in cl.properties.items():
        if getter.decl.implicit:
            continue

        emitter.emit_line(f'{{"{prop}",')
        emitter.emit_line(f" (getter){getter_name(cl, prop, emitter.names)},")

        if setter:
            emitter.emit_line(f" (setter){setter_name(cl, prop, emitter.names)},")
            emitter.emit_line("NULL, NULL},")
        else:
            emitter.emit_line("NULL, NULL, NULL},")

    if cl.has_dict:
        emitter.emit_line('{"__dict__", PyObject_GenericGetDict, PyObject_GenericSetDict},')

    emitter.emit_line("{NULL}  /* Sentinel */")
    emitter.emit_line("};")

