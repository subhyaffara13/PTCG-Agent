
def parse_native_yaml(
    path: str,
    tags_yaml_path: str,
    ignore_keys: set[DispatchKey] | None = None,
    *,
    skip_native_fns_gen: bool = False,
    loaded_yaml: object | None = None,
) -> ParsedYaml:
    global _GLOBAL_PARSE_NATIVE_YAML_CACHE
    if path not in _GLOBAL_PARSE_NATIVE_YAML_CACHE:
        valid_tags = parse_tags_yaml(tags_yaml_path)

        # if a loaded yaml is provided, use that instead of reading from path
        if loaded_yaml is None:
            with open(path) as f:
                es = yaml.load(f, Loader=LineLoader)
        else:
            es = loaded_yaml

        _GLOBAL_PARSE_NATIVE_YAML_CACHE[path] = parse_native_yaml_struct(
            es,
            valid_tags,
            ignore_keys,
            path=path,
            skip_native_fns_gen=skip_native_fns_gen,
        )

    return _GLOBAL_PARSE_NATIVE_YAML_CACHE[path]

