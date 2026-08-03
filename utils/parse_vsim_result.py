import json

def parse_vsim_result(response, **options):
    """
    Handle VSIM result since the command can be returning different result
    structures depending on input options.
    Parsing VSIM result into:
    - List[List[str]]
    - List[Dict[str, Number]] - when with_scores is used (without attributes)
    - List[Dict[str, Mapping[str, Any]]] - when with_attribs is used (without scores)
    - List[Dict[str, Union[Number, Mapping[str, Any]]]] - when with_scores and with_attribs are used

    """
    if response is None:
        return response

    withscores = bool(options.get(CallbacksOptions.WITHSCORES.value))
    withattribs = bool(options.get(CallbacksOptions.WITHATTRIBS.value))

    # Exactly one of withscores or withattribs is True
    if (withscores and not withattribs) or (not withscores and withattribs):
        # Redis will return a list of list of pairs.
        # This list have to be transformed to dict
        result_dict = {}
        if options.get(CallbacksOptions.RESP3.value):
            resp_dict = response
        else:
            resp_dict = pairs_to_dict(response)
        for key, value in resp_dict.items():
            if withscores:
                value = float(value)
            else:
                value = json.loads(value) if value else None

            result_dict[key] = value
        return result_dict
    elif withscores and withattribs:
        it = iter(response)
        result_dict = {}
        if options.get(CallbacksOptions.RESP3.value):
            for elem, data in response.items():
                if data[1] is not None:
                    attribs_dict = json.loads(data[1])
                else:
                    attribs_dict = None
                result_dict[elem] = {"score": data[0], "attributes": attribs_dict}
        else:
            for elem, score, attribs in zip(it, it, it):
                if attribs is not None:
                    attribs_dict = json.loads(attribs)
                else:
                    attribs_dict = None

                result_dict[elem] = {"score": float(score), "attributes": attribs_dict}
        return result_dict
    else:
        # return the list of elements for each level
        # list of lists
        return response

