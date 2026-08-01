
def _message_for(non_json):
    try:
        json.loads(non_json)
    except JSONDecodeError as error:
        return str(error)
    else:  # pragma: no cover
        raise RuntimeError("Tried and failed to capture a JSON dump error.")

