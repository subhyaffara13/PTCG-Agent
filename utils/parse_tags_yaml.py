
def parse_tags_yaml(path: str) -> set[str]:
    global _GLOBAL_PARSE_TAGS_YAML_CACHE
    if path not in _GLOBAL_PARSE_TAGS_YAML_CACHE:
        with open(path) as f:
            es = yaml.load(f, Loader=LineLoader)
            _GLOBAL_PARSE_TAGS_YAML_CACHE[path] = parse_tags_yaml_struct(es, path=path)

    return _GLOBAL_PARSE_TAGS_YAML_CACHE[path]

