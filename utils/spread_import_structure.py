
def spread_import_structure(nested_import_structure):
    """
    This method takes as input an unordered import structure and brings the required backends at the top-level,
    aggregating modules and objects under their required backends.

    Here's an example of an input import structure at the src.transformers.models level:

    {
        'albert': {
            frozenset(): {
                'configuration_albert': {'AlbertConfig'}
            },
            frozenset({'tokenizers'}): {
                'tokenization_albert_fast': {'AlbertTokenizer'}
            },
        },
        'align': {
            frozenset(): {
                'configuration_align': {'AlignConfig', 'AlignTextConfig', 'AlignVisionConfig'},
                'processing_align': {'AlignProcessor'}
            },
        },
        'altclip': {
            frozenset(): {
                'configuration_altclip': {'AltCLIPConfig', 'AltCLIPTextConfig', 'AltCLIPVisionConfig'},
                'processing_altclip': {'AltCLIPProcessor'},
            }
        }
    }

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

    """

    def propagate_frozenset(unordered_import_structure):
        frozenset_first_import_structure = {}
        for _key, _value in unordered_import_structure.items():
            # If the value is not a dict but a string, no need for custom manipulation
            if not isinstance(_value, dict):
                frozenset_first_import_structure[_key] = _value

            elif any(isinstance(v, frozenset) for v in _value):
                for k, v in _value.items():
                    if isinstance(k, frozenset):
                        # Here we want to switch around _key and k to propagate k upstream if it is a frozenset
                        if k not in frozenset_first_import_structure:
                            frozenset_first_import_structure[k] = {}
                        if _key not in frozenset_first_import_structure[k]:
                            frozenset_first_import_structure[k][_key] = {}

                        frozenset_first_import_structure[k][_key].update(v)

                    else:
                        # If k is not a frozenset, it means that the dictionary is not "level": some keys (top-level)
                        # are frozensets, whereas some are not -> frozenset keys are at an unknown depth-level of the
                        # dictionary.
                        #
                        # We recursively propagate the frozenset for this specific dictionary so that the frozensets
                        # are at the top-level when we handle them.
                        propagated_frozenset = propagate_frozenset({k: v})
                        for r_k, r_v in propagated_frozenset.items():
                            if isinstance(_key, frozenset):
                                if r_k not in frozenset_first_import_structure:
                                    frozenset_first_import_structure[r_k] = {}
                                if _key not in frozenset_first_import_structure[r_k]:
                                    frozenset_first_import_structure[r_k][_key] = {}

                                # _key is a frozenset -> we switch around the r_k and _key
                                frozenset_first_import_structure[r_k][_key].update(r_v)
                            else:
                                if _key not in frozenset_first_import_structure:
                                    frozenset_first_import_structure[_key] = {}
                                if r_k not in frozenset_first_import_structure[_key]:
                                    frozenset_first_import_structure[_key][r_k] = {}

                                # _key is not a frozenset -> we keep the order of r_k and _key
                                frozenset_first_import_structure[_key][r_k].update(r_v)

            else:
                frozenset_first_import_structure[_key] = propagate_frozenset(_value)

        return frozenset_first_import_structure

    def flatten_dict(_dict, previous_key=None):
        items = []
        for _key, _value in _dict.items():
            _key = f"{previous_key}.{_key}" if previous_key is not None else _key
            if isinstance(_value, dict):
                items.extend(flatten_dict(_value, _key).items())
            else:
                items.append((_key, _value))
        return dict(items)

    # The tuples contain the necessary backends. We want these first, so we propagate them up the
    # import structure.
    ordered_import_structure = nested_import_structure

    # 6 is a number that gives us sufficient depth to go through all files and foreseeable folder depths
    # while not taking too long to parse.
    for i in range(6):
        ordered_import_structure = propagate_frozenset(ordered_import_structure)

    # We then flatten the dict so that it references a module path.
    flattened_import_structure = {}
    for key, value in ordered_import_structure.copy().items():
        if isinstance(key, str):
            del ordered_import_structure[key]
        else:
            flattened_import_structure[key] = flatten_dict(value)

    return flattened_import_structure

