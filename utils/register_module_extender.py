
def register_module_extender(
    manager: AstroidManager, module_name: str, get_extension_mod: Callable[[], Module]
) -> None:
    def transform(node: Module) -> None:
        extension_module = get_extension_mod()
        for name, objs in extension_module.locals.items():
            node.locals[name] = objs
            for obj in objs:
                if obj.parent is extension_module:
                    obj.parent = node

    manager.register_transform(Module, transform, lambda n: n.name == module_name)

