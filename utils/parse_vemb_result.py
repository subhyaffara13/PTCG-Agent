
def parse_vemb_result(response, **options):
    """
    Handle VEMB result since the command can returning different result
    structures depending on input options and on quantization type of the vector set.

    Parsing VEMB result into:
    - List[Union[bytes, Union[int, float]]]
    - Dict[str, Union[bytes, str, float]]
    """
    if response is None:
        return response

    if options.get(CallbacksOptions.RAW.value):
        result = {}
        result["quantization"] = (
            response[0].decode("utf-8")
            if options.get(CallbacksOptions.ALLOW_DECODING.value)
            else response[0]
        )
        result["raw"] = response[1]
        result["l2"] = float(response[2])
        if len(response) > 3:
            result["range"] = float(response[3])
        return result
    else:
        if options.get(CallbacksOptions.RESP3.value):
            return response

        result = []
        for i in range(len(response)):
            try:
                result.append(int(response[i]))
            except ValueError:
                # if the value is not an integer, it should be a float
                result.append(float(response[i]))

        return result

