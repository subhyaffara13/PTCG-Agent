import os
import pathlib

def append_dir_sep(path: pathlib.Path) -> str:
	"""
	Appends the path separator to the path if the path is a directory. This can be
	used to aid in distinguishing between directories and files on the file-system
	by relying on the presence of a trailing path separator.

	*path* (:class:`pathlib.Path`) is the path to use.

	Returns the path (:class:`str`).
	"""
	str_path = str(path)
	if path.is_dir():
		str_path += os.sep

	return str_path

