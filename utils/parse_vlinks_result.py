
def parse_vlinks_result(response, **options):
    """
    Handle VLINKS result since the command can be returning different result
    structures depending on input options.
    Parsing VLINKS result into:
    - List[List[str]]
    - List[Dict[str, Number]]
    """
    if response is None:
        return response

    if options.get(CallbacksOptions.WITHSCORES.value):
        result = []
        # Redis will return a list of list of strings.
        # This list have to be transformed to list of dicts
        for level_item in response:
            level_data_dict = {}
            for key, value in pairs_to_dict(level_item).items():
                value = float(value)
                level_data_dict[key] = value
            result.append(level_data_dict)
        return result
    else:
        # return the list of elements for each level
        # list of lists
        return response

