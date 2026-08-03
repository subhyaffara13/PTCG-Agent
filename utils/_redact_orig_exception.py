from typing import Union

def _redact_orig_exception(
    orig_exception: Union[requests.exceptions.HTTPError, str],
) -> Union[requests.exceptions.HTTPError, str]:
    if isinstance(orig_exception, requests.exceptions.HTTPError):
        return requests.exceptions.HTTPError(
            redact_string(str(orig_exception)), response=orig_exception.response
        )
    return redact_string(str(orig_exception))

