
def check_match_file(
	patterns: Iterable[tuple[int, Pattern]],
	file: str,
	is_reversed: Optional[bool] = None,
) -> tuple[Optional[bool], Optional[int]]:
	"""
	Check the file against the patterns.

	*patterns* (:class:`~collections.abc.Iterable`) yields each indexed pattern
	(:class:`tuple`) which contains the pattern index (:class:`int`) and actua
	pattern (:class:`.Pattern`).

	*file* (:class:`str`) is the normalized file path to be matched against
	*patterns*.

	*is_reversed* (:class:`bool` or :data:`None`) is whether the order of the
	patterns has been reversed. Default is :data:`None` for :data:`False`.
	Reversing the order of the patterns is an optimization.

	Returns a :class:`tuple` containing whether to include *file* (:class:`bool`
	or :data:`None`), and the index of the last matched pattern (:class:`int` or
	:data:`None`).
	"""
	if is_reversed:
		# Check patterns in reverse order. The first pattern that matches takes
		# precedence.
		for index, pattern in patterns:
			if pattern.include is not None and pattern.match_file(file) is not None:
				return pattern.include, index

		return None, None

	else:
		# Check all patterns. The last pattern that matches takes precedence.
		out_include: Optional[bool] = None
		out_index: Optional[int] = None
		for index, pattern in patterns:
			if pattern.include is not None and pattern.match_file(file) is not None:
				out_include = pattern.include
				out_index = index

		return out_include, out_index

