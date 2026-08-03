import os

def write_and_fudge_mtime(content: str, target_path: str) -> None:
    # In some systems, mtime has a resolution of 1 second which can
    # cause annoying-to-debug issues when a file has the same size
    # after a change. We manually set the mtime to circumvent this.
    # Note that we increment the old file's mtime, which guarantees a
    # different value, rather than incrementing the mtime after the
    # copy, which could leave the mtime unchanged if the old file had
    # a similarly fudged mtime.
    new_time = None
    if os.path.isfile(target_path):
        new_time = os.stat(target_path).st_mtime + 1

    dir = os.path.dirname(target_path)
    os.makedirs(dir, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as target:
        target.write(content)

    if new_time:
        os.utime(target_path, times=(new_time, new_time))

