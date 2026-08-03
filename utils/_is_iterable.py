from typing import Any

def _is_iterable(value: Any) -> bool:
	"""
	Check whether the value is an iterable (excludes strings).

	*value* is the value to check,

	Returns whether *value* is an iterable (:class:`bool`).
	"""
	return isinstance(value, Iterable) and not isinstance(value, (str, bytes))


def _is_iterable(obj, _str_type=(str, bytes), _iter_exception=Exception):
    # str's are iterable, but in pyparsing, we don't want to iterate over them
    if isinstance(obj, _str_type):
        return False

    try:
        iter(obj)
    except _iter_exception:  # noqa
        return False
    else:
        return True

