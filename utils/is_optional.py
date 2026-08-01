
def is_optional(ann):
    if ann is Optional:
        raise_error_container_parameter_missing("Optional")

    def is_optional_as_optional(ann):
        return (
            hasattr(ann, "__module__")
            and ann.__module__ == "typing"
            and (get_origin(ann) is Optional)
        )

    def is_union_as_optional(ann):
        ann_args = get_args(ann)
        return len(ann_args) == 2 and (None in ann_args or type(None) in ann_args)

    return is_optional_as_optional(ann) or (is_union(ann) and is_union_as_optional(ann))


def is_optional(config_path: str, config: Any) -> bool:
  raw_type = get_type(config_path, config, normalize=False)
  return extract_type_from_optional(raw_type) is not None

