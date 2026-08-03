import os
from pathlib import Path


def _can_symlink_files(base_dir: Path) -> bool:
    with TemporaryDirectory(dir=str(base_dir.resolve())) as tmp:
        path1, path2 = Path(tmp, "file1.txt"), Path(tmp, "file2.txt")
        path1.write_text("file1", encoding="utf-8")
        with suppress(AttributeError, NotImplementedError, OSError):
            os.symlink(path1, path2)
            if path2.is_symlink() and path2.read_text(encoding="utf-8") == "file1":
                return True

        try:
            os.link(path1, path2)  # Ensure hard links can be created
        except Exception as ex:
            msg = (
                "File system does not seem to support either symlinks or hard links. "
                "Strict editable installs require one of them to be supported."
            )
            raise LinksNotSupported(msg) from ex
        return False

