import os
from typing import Optional

def normalize_file(
	file: StrPath,
	separators: Optional[Collection[str]] = None,
) -> str:
	"""
	Normalizes the file path to use the POSIX path separator (i.e., ``"/"``), and
	make the paths relative (remove leading ``"/"``).

	*file* (:class:`str` or :class:`os.PathLike`) is the file path.

	*separators* (:class:`~collections.abc.Collection` of :class:`str`; or
	:data:`None`) optionally contains the path separators to normalize. This does
	not need to include the POSIX path separator (``"/"``), but including it will
	not affect the results. Default is ``None`` for :data:`.NORMALIZE_PATH_SEPS`.
	To prevent normalization, pass an empty container (e.g., an empty tuple
	``()``).

	Returns the normalized file path (:class:`str`).
	"""
	# Normalize path separators.
	if separators is None:
		separators = NORMALIZE_PATH_SEPS

	assert separators is not None, separators

	# Convert path object to string.
	norm_file: str = os.fspath(file)

	for sep in separators:
		norm_file = norm_file.replace(sep, posixpath.sep)

	if norm_file.startswith('/'):
		# Make path relative.
		norm_file = norm_file[1:]

	elif norm_file.startswith('./'):
		# Remove current directory prefix.
		norm_file = norm_file[2:]

	return norm_file

