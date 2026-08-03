from typing import Callable

def lookup_pattern(name: str) -> Callable[[AnyStr], Pattern]:
	"""
	Looks up a registered pattern factory by name.

	*name* (:class:`str`) is the name of the pattern factory.

	Returns the registered pattern factory (:class:`~collections.abc.Callable`).
	If no pattern factory is registered, raises :exc:`KeyError`.
	"""
	return _registered_patterns[name]  # type: ignore[return-value]

