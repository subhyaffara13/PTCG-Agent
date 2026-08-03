import os
from pathlib import Path


def make_file_manager(
    options: Namespace,
    install_dir: str | Path | None = None,
) -> FileManager:
    template_dir = os.path.join(options.source_path, "templates")
    install_dir = install_dir if install_dir else options.install_dir
    return FileManager(
        install_dir=install_dir,
        template_dir=template_dir,
        dry_run=options.dry_run,
    )

