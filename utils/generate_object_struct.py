
def generate_object_struct(cl: ClassIR, emitter: Emitter) -> None:
    seen_attrs: set[str] = set()
    lines: list[str] = []
    lines += ["typedef struct {", "PyObject_HEAD", "CPyVTableItem *vtable;"]
    if cl.has_method("__call__"):
        lines.append("vectorcallfunc vectorcall;")
    bitmap_attrs = []
    for base in reversed(cl.base_mro):
        if not base.is_trait:
            if base.bitmap_attrs:
                # Do we need another attribute bitmap field?
                if emitter.bitmap_field(len(base.bitmap_attrs) - 1) not in bitmap_attrs:
                    for i in range(0, len(base.bitmap_attrs), BITMAP_BITS):
                        attr = emitter.bitmap_field(i)
                        if attr not in bitmap_attrs:
                            lines.append(f"{BITMAP_TYPE} {attr};")
                            bitmap_attrs.append(attr)
            for attr, rtype in base.attributes.items():
                # Generated class may redefine certain attributes with different
                # types in subclasses (this would be unsafe for user-defined classes).
                if attr not in seen_attrs:
                    lines.append(f"{emitter.ctype_spaced(rtype)}{emitter.attr(attr)};")
                    seen_attrs.add(attr)

                    if isinstance(rtype, RTuple):
                        emitter.declare_tuple_struct(rtype)

    lines.append(f"}} {cl.struct_name(emitter.names)};")
    lines.append("")
    emitter.context.declarations[cl.struct_name(emitter.names)] = HeaderDeclaration(
        lines, is_type=True
    )

