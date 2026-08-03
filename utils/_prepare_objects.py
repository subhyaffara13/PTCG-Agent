from pathlib import Path


def _prepare_objects(mname, objects, bdir):
    Path(bdir).mkdir(parents=True, exist_ok=True)
    # Copy objects
    for obj in objects:
        if Path(obj).exists() and Path(obj).is_file():
            shutil.copy(obj, bdir)

