
def _import_string_logic(dotted_path: str) -> Any:
    """Inspired by uvicorn — dotted paths should include a colon before the final item if that item is not a module.
    (This is necessary to distinguish between a submodule and an attribute when there is a conflict.).

    If the dotted path does not include a colon and the final item is not a valid module, importing as an attribute
    rather than a submodule will be attempted automatically.

    So, for example, the following values of `dotted_path` result in the following returned values:
    * 'collections': <module 'collections'>
    * 'collections.abc': <module 'collections.abc'>
    * 'collections.abc:Mapping': <class 'collections.abc.Mapping'>
    * `collections.abc.Mapping`: <class 'collections.abc.Mapping'> (though this is a bit slower than the previous line)

    An error will be raised under any of the following scenarios:
    * `dotted_path` contains more than one colon (e.g., 'collections:abc:Mapping')
    * the substring of `dotted_path` before the colon is not a valid module in the environment (e.g., '123:Mapping')
    * the substring of `dotted_path` after the colon is not an attribute of the module (e.g., 'collections:abc123')
    """
    from importlib import import_module

    components = dotted_path.strip().split(':')
    if len(components) > 2:
        raise ImportError(f"Import strings should have at most one ':'; received {dotted_path!r}")
    attribute = None
    if len(components) == 2:
        attribute = components[1]
    module_path = components[0]
    if not module_path:
        raise ImportError(f'Import strings should have a nonempty module name; received {dotted_path!r}')

    try:
        module = import_module(module_path)
    except ModuleNotFoundError:
        if attribute is None and '.' in module_path:
            # Try interpreting the final dotted segment as an attribute, not a submodule
            maybe_module_path, maybe_attribute = module_path.rsplit('.', 1)

            try:
                return _import_string_logic(f'{maybe_module_path}:{maybe_attribute}')
            except ImportError:
                pass
        raise

    if attribute is not None:
        try:
            return getattr(module, attribute)
        except AttributeError as e:
            raise ImportError(f'cannot import name {attribute!r} from {module_path!r}') from e
    else:
        return module

