from typing import Optional

def detailed_match_files(
	patterns: Iterable[Pattern],
	files: Iterable[str],
	all_matches: Optional[bool] = None,
) -> dict[str, MatchDetail]:
	"""
	Matches the files to the patterns, and returns which patterns matched the
	files.

	*patterns* (:class:`~collections.abc.Iterable` of :class:`.Pattern`) contains
	the patterns to use.

	*files* (:class:`~collections.abc.Iterable` of :class:`str`) contains the
	normalized file paths to be matched against *patterns*.

	*all_matches* (:class:`bool` or :data:`None`) is whether to return all matches
	patterns (:data:`True`), or only the last matched pattern (:data:`False`).
	Default is :data:`None` for :data:`False`.

	Returns the matched files (:class:`dict`) which maps each matched file
	(:class:`str`) to the patterns that matched in order (:class:`.MatchDetail`).
	"""
	all_files = files if isinstance(files, Collection) else list(files)
	return_files: dict[str, MatchDetail] = {}
	for pattern in patterns:
		if pattern.include is not None:
			result_files = pattern.match(all_files)  # TODO: Replace with `.match_file()`.
			if pattern.include:
				# Add files and record pattern.
				for result_file in result_files:
					if result_file in return_files:
						# We know here that .patterns is a list, because we made it here
						if all_matches:
							return_files[result_file].patterns.append(pattern)  # type: ignore[attr-defined]
						else:
							return_files[result_file].patterns[0] = pattern  # type: ignore[index]
					else:
						return_files[result_file] = MatchDetail([pattern])

			else:
				# Remove files.
				for file in result_files:
					del return_files[file]

	return return_files

