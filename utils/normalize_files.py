
def normalize_files(
	files: Iterable[StrPath],
	separators: Optional[Collection[str]] = None,
) -> dict[str, list[StrPath]]:
	"""
	.. version-deprecated:: 0.10.0
		This function is no longer used. Use the :func:`.normalize_file` function
		with a loop for better results.

	Normalizes the file paths to use the POSIX path separator.

	*files* (:class:`~collections.abc.Iterable` of :class:`str` or
	:class:`os.PathLike`) contains the file paths to be normalized.

	*separators* (:class:`~collections.abc.Collection` of :class:`str`; or
	:data:`None`) optionally contains the path separators to normalize. See
	:func:`.normalize_file` for more information.

	Returns a :class:`dict` mapping each normalized file path (:class:`str`) to
	the original file paths (:class:`list` of :class:`str` or
	:class:`os.PathLike`).
	"""
	norm_files: dict[str, list[StrPath]] = {}
	for path in files:
		norm_file = normalize_file(path, separators=separators)
		if norm_file in norm_files:
			norm_files[norm_file].append(path)
		else:
			norm_files[norm_file] = [path]

	return norm_files

