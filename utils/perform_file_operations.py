import os

def perform_file_operations(operations: list[UpdateFile | DeleteFile]) -> None:
    for op in operations:
        if isinstance(op, UpdateFile):
            # Modify/create file
            write_and_fudge_mtime(op.content, op.target_path)
        else:
            # Delete file/directory
            if os.path.isdir(op.path):
                # Sanity check to avoid unexpected deletions
                assert op.path.startswith("tmp")
                shutil.rmtree(op.path)
            else:
                # Use retries to work around potential flakiness on Windows (AppVeyor).
                path = op.path
                retry_on_error(lambda: os.remove(path))

