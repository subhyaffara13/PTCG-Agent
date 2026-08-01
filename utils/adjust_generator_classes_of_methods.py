
def adjust_generator_classes_of_methods(mapper: Mapper) -> None:
    """Make optimizations and adjustments to generated generator classes of methods.

    This is a separate pass after type map has been built, since we need all classes
    to be processed to analyze class hierarchies.
    """

    generator_methods = []

    for fdef, fn_ir in mapper.func_to_decl.items():
        if isinstance(fdef, FuncDef) and (fdef.is_coroutine or fdef.is_generator):
            gen_ir = create_generator_class_for_func(
                fn_ir.module_name, fn_ir.class_name, fdef, mapper
            )
            # TODO: We could probably support decorators sometimes (static and class method?)
            if not fdef.is_decorated:
                name = fn_ir.name
                precise_ret_type = True
                if fn_ir.class_name is not None:
                    class_ir = mapper.type_to_ir[fdef.info]
                    subcls = class_ir.subclasses()
                    if subcls is None:
                        # Override could be of a different type, so we can't make assumptions.
                        precise_ret_type = False
                    elif class_ir.is_trait:
                        # Give up on traits. We could possibly have an abstract base class
                        # for generator return types to make this use precise types.
                        precise_ret_type = False
                    else:
                        for s in subcls:
                            if name in s.method_decls:
                                m = s.method_decls[name]
                                if (
                                    m.is_generator != fn_ir.is_generator
                                    or m.is_coroutine != fn_ir.is_coroutine
                                ):
                                    # Override is of a different kind, and the optimization
                                    # to use a precise generator return type doesn't work.
                                    precise_ret_type = False
                else:
                    class_ir = None

                if precise_ret_type:
                    # Give a more precise type for generators, so that we can optimize
                    # code that uses them. They return a generator object, which has a
                    # specific class. Without this, the type would have to be 'object'.
                    fn_ir.sig.ret_type = RInstance(gen_ir)
                    if fn_ir.bound_sig:
                        fn_ir.bound_sig.ret_type = RInstance(gen_ir)
                    if class_ir is not None:
                        if class_ir.is_method_final(name):
                            gen_ir.is_final_class = True
                        generator_methods.append((name, class_ir, gen_ir))

    new_bases = {}

    for name, class_ir, gen in generator_methods:
        # For generator methods, we need to have subclass generator classes inherit from
        # baseclass generator classes when there are overrides to maintain LSP.
        base = class_ir.real_base()
        if base is not None:
            if base.has_method(name):
                base_sig = base.method_sig(name)
                if isinstance(base_sig.ret_type, RInstance):
                    base_gen = base_sig.ret_type.class_ir
                    new_bases[gen] = base_gen

    # Add generator inheritance relationships by adjusting MROs.
    for deriv, base in new_bases.items():
        if base.children is not None:
            base.children.append(deriv)
        while True:
            deriv.mro.append(base)
            deriv.base_mro.append(base)
            if base not in new_bases:
                break
            base = new_bases[base]

