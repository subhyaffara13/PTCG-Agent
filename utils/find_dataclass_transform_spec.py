
def find_dataclass_transform_spec(node: Node | None) -> DataclassTransformSpec | None:
    """
    Find the dataclass transform spec for the given node, if any exists.

    Per PEP 681 (https://peps.python.org/pep-0681/#the-dataclass-transform-decorator), dataclass
    transforms can be specified in multiple ways, including decorator functions and
    metaclasses/base classes. This function resolves the spec from any of these variants.
    """

    # The spec only lives on the function/class definition itself, so we need to unwrap down to that
    # point
    if isinstance(node, CallExpr):
        # Like dataclasses.dataclass, transform-based decorators can be applied either with or
        # without parameters; ie, both of these forms are accepted:
        #
        # @typing.dataclass_transform
        # class Foo: ...
        # @typing.dataclass_transform(eq=True, order=True, ...)
        # class Bar: ...
        #
        # We need to unwrap the call for the second variant.
        node = node.callee

    if isinstance(node, RefExpr):
        node = node.node

    if isinstance(node, Decorator):
        # typing.dataclass_transform usage must always result in a Decorator; it always uses the
        # `@dataclass_transform(...)` syntax and never `@dataclass_transform`
        node = node.func

    if isinstance(node, OverloadedFuncDef):
        # The dataclass_transform decorator may be attached to any single overload, so we must
        # search them all.
        # Note that using more than one decorator is undefined behavior, so we can just take the
        # first that we find.
        for candidate in node.items:
            spec = find_dataclass_transform_spec(candidate)
            if spec is not None:
                return spec
        return find_dataclass_transform_spec(node.impl)

    # For functions, we can directly consult the AST field for the spec
    if isinstance(node, FuncDef):
        return node.dataclass_transform_spec

    if isinstance(node, ClassDef):
        node = node.info
    if isinstance(node, TypeInfo):
        # Search all parent classes to see if any are decorated with `typing.dataclass_transform`
        for base in node.mro[1:]:
            if base.dataclass_transform_spec is not None:
                return base.dataclass_transform_spec

        # Check if there is a metaclass that is decorated with `typing.dataclass_transform`
        #
        # Note that PEP 681 only discusses using a metaclass that is directly decorated with
        # `typing.dataclass_transform`; subclasses thereof should be treated with dataclass
        # semantics rather than as transforms:
        #
        # > If dataclass_transform is applied to a class, dataclass-like semantics will be assumed
        # > for any class that directly or indirectly derives from the decorated class or uses the
        # > decorated class as a metaclass.
        #
        # The wording doesn't make this entirely explicit, but Pyright (the reference
        # implementation for this PEP) only handles directly-decorated metaclasses.
        metaclass_type = node.metaclass_type
        if metaclass_type is not None and metaclass_type.type.dataclass_transform_spec is not None:
            return metaclass_type.type.dataclass_transform_spec

    return None

