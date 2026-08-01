
def _clean_schema_for_pretty_print(obj: Any, strip_metadata: bool = True) -> Any:  # pragma: no cover
    """A utility function to remove irrelevant information from a core schema."""
    if isinstance(obj, Mapping):
        new_dct = {}
        for k, v in obj.items():
            if k == 'metadata' and strip_metadata:
                new_metadata = {}

                for meta_k, meta_v in v.items():
                    if meta_k in ('pydantic_js_functions', 'pydantic_js_annotation_functions'):
                        new_metadata['js_metadata'] = '<stripped>'
                    else:
                        new_metadata[meta_k] = _clean_schema_for_pretty_print(meta_v, strip_metadata=strip_metadata)

                if list(new_metadata.keys()) == ['js_metadata']:
                    new_metadata = {'<stripped>'}

                new_dct[k] = new_metadata
            # Remove some defaults:
            elif k in ('custom_init', 'root_model') and not v:
                continue
            else:
                new_dct[k] = _clean_schema_for_pretty_print(v, strip_metadata=strip_metadata)

        return new_dct
    elif isinstance(obj, Sequence) and not isinstance(obj, str):
        return [_clean_schema_for_pretty_print(v, strip_metadata=strip_metadata) for v in obj]
    else:
        return obj

