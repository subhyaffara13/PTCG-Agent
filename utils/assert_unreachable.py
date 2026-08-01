
def assert_unreachable(message: str) -> Never:
	"""
	The code path is unreachable. Raises an :class:`AssertionError`.

	*message* (:class:`str`) is the error message.
	"""
	raise AssertionError(message)

