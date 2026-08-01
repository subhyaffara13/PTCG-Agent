
def _update_dictionary(existing_dict: Dict, new_dict: dict) -> dict:
    for k, v in new_dict.items():
        if v is not None:
            # Convert stringified numbers to appropriate numeric types
            if isinstance(v, str):
                existing_dict[k] = _convert_stringified_numbers(v)
            elif isinstance(v, dict):
                existing_nested_dict = existing_dict.get(k)
                if isinstance(existing_nested_dict, dict):
                    existing_nested_dict.update(v)
                    existing_dict[k] = existing_nested_dict
                else:
                    existing_dict[k] = v
            else:
                existing_dict[k] = v

    return existing_dict

