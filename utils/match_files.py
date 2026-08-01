
def match_files(
	patterns: Iterable[Pattern],
	files: Iterable[str],
) -> set[str]:
	"""
	.. version-deprecated:: 0.10.0
		This function is no longer used. Use the :func:`.match_file` function with a
		loop for better results.

	Matches the files to the patterns.

	*patterns* (:class:`~collections.abc.Iterable` of :class:`.Pattern`) contains
	the patterns to use.

	*files* (:class:`~collections.abc.Iterable` of :class:`str`) contains the
	normalized file paths to be matched against *patterns*.

	Returns the matched files (:class:`set` of :class:`str`).
	"""
	use_patterns = [__pat for __pat in patterns if __pat.include is not None]

	return_files = set()
	for file in files:
		if match_file(use_patterns, file):
			return_files.add(file)

	return return_files

