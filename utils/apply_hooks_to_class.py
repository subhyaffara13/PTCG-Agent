
def apply_hooks_to_class(
    self: SemanticAnalyzer,
    module: str,
    info: TypeInfo,
    options: Options,
    file_node: MypyFile,
    errors: Errors,
) -> bool:
    # TODO: Move more class-related hooks here?
    defn = info.defn
    ok = True
    for decorator in defn.decorators:
        with self.file_context(file_node, options, info):
            hook = None

            decorator_name = self.get_fullname_for_hook(decorator)
            if decorator_name:
                hook = self.plugin.get_class_decorator_hook_2(decorator_name)
            # Special case: if the decorator is itself decorated with
            # typing.dataclass_transform, apply the hook for the dataclasses plugin
            # TODO: remove special casing here
            if hook is None and find_dataclass_transform_spec(decorator):
                hook = dataclasses_plugin.dataclass_class_maker_callback

            if hook:
                ok = ok and hook(ClassDefContext(defn, decorator, self))

    # Check if the class definition itself triggers a dataclass transform (via a parent class/
    # metaclass)
    spec = find_dataclass_transform_spec(info)
    if spec is not None:
        with self.file_context(file_node, options, info):
            # We can't use the normal hook because reason = defn, and ClassDefContext only accepts
            # an Expression for reason
            ok = ok and dataclasses_plugin.DataclassTransformer(defn, defn, spec, self).transform()

    return ok

