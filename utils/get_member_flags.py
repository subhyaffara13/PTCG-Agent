
def get_member_flags(name: str, itype: Instance, class_obj: bool = False) -> set[int]:
    """Detect whether a member 'name' is settable, whether it is an
    instance or class variable, and whether it is class or static method.

    The flags are defined as following:
    * IS_SETTABLE: whether this attribute can be set, not set for methods and
      non-settable properties;
    * IS_CLASSVAR: set if the variable is annotated as 'x: ClassVar[t]';
    * IS_CLASS_OR_STATIC: set for methods decorated with @classmethod or
      with @staticmethod.
    """
    info = itype.type
    method = info.get_method(name)
    setattr_meth = info.get_method("__setattr__")
    if method:
        if isinstance(method, Decorator):
            if method.var.is_staticmethod or method.var.is_classmethod:
                return {IS_CLASS_OR_STATIC}
            elif method.var.is_property:
                return {IS_VAR}
        elif method.is_property:  # this could be settable property
            assert isinstance(method, OverloadedFuncDef)
            dec = method.items[0]
            assert isinstance(dec, Decorator)
            if dec.var.is_settable_property or setattr_meth:
                flags = {IS_VAR, IS_SETTABLE}
                if dec.var.setter_type is not None:
                    flags.add(IS_EXPLICIT_SETTER)
                return flags
            else:
                return {IS_VAR}
        return set()  # Just a regular method
    node = info.get(name)
    if not node:
        if setattr_meth:
            return {IS_SETTABLE}
        if itype.extra_attrs and name in itype.extra_attrs.attrs:
            flags = set()
            if name not in itype.extra_attrs.immutable:
                flags.add(IS_SETTABLE)
            return flags
        return set()
    v = node.node
    # just a variable
    if isinstance(v, Var):
        if v.is_property:
            return {IS_VAR}
        flags = {IS_VAR}
        if not v.is_final:
            flags.add(IS_SETTABLE)
        # TODO: define cleaner rules for class vs instance variables.
        if v.is_classvar and not is_descriptor(v.type):
            flags.add(IS_CLASSVAR)
        if class_obj and v.is_inferred:
            flags.add(IS_CLASSVAR)
        return flags
    return set()

