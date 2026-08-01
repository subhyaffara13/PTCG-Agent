
def generate_getseter_declarations(cl: ClassIR, emitter: Emitter) -> None:
    if not cl.is_trait:
        for attr in cl.attributes:
            emitter.emit_line("static PyObject *")
            emitter.emit_line(
                "{}({} *self, void *closure);".format(
                    getter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
                )
            )
            # Final attributes are read-only, so they have no setter.
            if attr not in cl.final_attributes:
                emitter.emit_line("static int")
                emitter.emit_line(
                    "{}({} *self, PyObject *value, void *closure);".format(
                        setter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
                    )
                )

    for prop, (getter, setter) in cl.properties.items():
        if getter.decl.implicit:
            continue

        # Generate getter declaration
        emitter.emit_line("static PyObject *")
        emitter.emit_line(
            "{}({} *self, void *closure);".format(
                getter_name(cl, prop, emitter.names), cl.struct_name(emitter.names)
            )
        )

        # Generate property setter declaration if a setter exists
        if setter:
            emitter.emit_line("static int")
            emitter.emit_line(
                "{}({} *self, PyObject *value, void *closure);".format(
                    setter_name(cl, prop, emitter.names), cl.struct_name(emitter.names)
                )
            )

