import os
import sys

def copy_output_files(target_dir: str) -> None:
    try:
        os.mkdir(target_dir)
    except OSError:
        # Only copy data for the first failure, to avoid excessive output in case
        # many tests fail
        return

    for fnam in glob.glob("build/*.[ch]"):
        shutil.copy(fnam, target_dir)

    sys.stderr.write(f"\nGenerated files: {target_dir} (for first failure only)\n\n")

