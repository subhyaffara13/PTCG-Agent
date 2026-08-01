
def match_file(patterns: Iterable[Pattern], file: str) -> bool:
	"""
	Matches the file to the patterns.

	*patterns* (:class:`~collections.abc.Iterable` of :class:`.Pattern`) contains
	the patterns to use.

	*file* (:class:`str`) is the normalized file path to be matched against
	*patterns*.

	Returns :data:`True` if *file* matched; otherwise, :data:`False`.
	"""
	matched = False
	for pattern in patterns:
		if pattern.include is not None and pattern.match_file(file) is not None:
			matched = pattern.include

	return matched

