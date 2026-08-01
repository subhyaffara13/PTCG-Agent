
def generate_class_type_decl(
    cl: ClassIR, c_emitter: Emitter, external_emitter: Emitter, emitter: Emitter
) -> None:
    context = c_emitter.context
    name = emitter.type_struct_name(cl)
    context.declarations[name] = HeaderDeclaration(
        f"PyTypeObject *{emitter.type_struct_name(cl)};", needs_export=True
    )

    # If this is a non-extension class, all we want is the type object decl.
    if not cl.is_ext_class:
        return

    generate_object_struct(cl, external_emitter)
    generate_full = not cl.is_trait and not cl.builtin_base
    if generate_full:
        context.declarations[emitter.native_function_name(cl.ctor)] = HeaderDeclaration(
            f"{native_function_header(cl.ctor, emitter)};", needs_export=True
        )

