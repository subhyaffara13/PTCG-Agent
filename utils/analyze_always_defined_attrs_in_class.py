
def analyze_always_defined_attrs_in_class(cl: ClassIR, seen: set[ClassIR]) -> None:
    if cl in seen:
        return

    seen.add(cl)

    if (
        cl.is_trait
        or cl.inherits_python
        or cl.allow_interpreted_subclasses
        or cl.builtin_base is not None
        or cl.children is None
        or cl.is_serializable()
        or cl.has_method("__new__")
    ):
        # Give up -- we can't enforce that attributes are always defined.
        return

    # First analyze all base classes. Track seen classes to avoid duplicate work.
    for base in cl.mro[1:]:
        analyze_always_defined_attrs_in_class(base, seen)

    m = cl.get_method("__init__")
    if m is None:
        cl._always_initialized_attrs = cl.attrs_with_defaults.copy()
        cl._sometimes_initialized_attrs = cl.attrs_with_defaults.copy()
        return
    self_reg = m.arg_regs[0]
    cfg = get_cfg(m.blocks)
    dirty = analyze_self_leaks(m.blocks, self_reg, cfg)
    maybe_defined = analyze_maybe_defined_attrs_in_init(
        m.blocks, self_reg, cl.attrs_with_defaults, cfg
    )
    all_attrs: set[str] = set()
    for base in cl.mro:
        all_attrs.update(base.attributes)
    maybe_undefined = analyze_maybe_undefined_attrs_in_init(
        m.blocks, self_reg, initial_undefined=all_attrs - cl.attrs_with_defaults, cfg=cfg
    )

    always_defined = find_always_defined_attributes(
        m.blocks, self_reg, all_attrs, maybe_defined, maybe_undefined, dirty
    )
    always_defined = {a for a in always_defined if not cl.is_deletable(a)}

    cl._always_initialized_attrs = always_defined
    if dump_always_defined:
        print(cl.name, sorted(always_defined))
    cl._sometimes_initialized_attrs = find_sometimes_defined_attributes(
        m.blocks, self_reg, maybe_defined, dirty
    )

    mark_attr_initialization_ops(m.blocks, self_reg, maybe_defined, dirty)

    # Check if __init__ can run unpredictable code (leak 'self').
    any_dirty = False
    for b in m.blocks:
        for i, op in enumerate(b.ops):
            if dirty.after[b, i] and not isinstance(op, Return):
                any_dirty = True
                break
    cl.init_self_leak = any_dirty

