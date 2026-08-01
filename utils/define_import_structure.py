
def define_import_structure(module_path: str, prefix: str | None = None) -> IMPORT_STRUCTURE_T:
    """
    This method takes a module_path as input and creates an import structure digestible by a _LazyModule.

    Here's an example of an output import structure at the src.transformers.models level:

    {
        frozenset({'tokenizers'}): {
            'albert.tokenization_albert_fast': {'AlbertTokenizer'}
        },
        frozenset(): {
            'albert.configuration_albert': {'AlbertConfig'},
            'align.processing_align': {'AlignProcessor'},
            'align.configuration_align': {'AlignConfig', 'AlignTextConfig', 'AlignVisionConfig'},
            'altclip.configuration_altclip': {'AltCLIPConfig', 'AltCLIPTextConfig', 'AltCLIPVisionConfig'},
            'altclip.processing_altclip': {'AltCLIPProcessor'}
        }
    }

    The import structure is a dict defined with frozensets as keys, and dicts of strings to sets of objects.

    If `prefix` is not None, it will add that prefix to all keys in the returned dict.
    """
    import_structure = create_import_structure_from_path(module_path)
    spread_dict = spread_import_structure(import_structure)

    if prefix is None:
        return spread_dict
    else:
        spread_dict = {k: {f"{prefix}.{kk}": vv for kk, vv in v.items()} for k, v in spread_dict.items()}
        return spread_dict

