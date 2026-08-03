import os
import subprocess
from typing import Any
from pathlib import Path


def _worker_task_halide(lockfile: str, jobs: list[partial[Any]]) -> None:
    from torch.utils._filelock import FileLock

    try:
        with FileLock(lockfile, LOCK_TIMEOUT):
            for job in jobs:
                job()
    except subprocess.SubprocessError as e:
        if os.environ.get("HALIDE_REPRO") == "1":
            cmd: list[Any]
            python, script, *cmd = getattr(e, "cmd", ("", "", ""))
            if os.path.basename(python).startswith("python"):
                code = Path(script).read_text()
                main = "    hl.main()"
                assert code.count(main) == 1

                class Out:
                    def __repr__(self) -> str:
                        return "out"

                ci = cmd.index("-o")
                assert isinstance(ci, int)
                # pyrefly: ignore [unsupported-operation]
                cmd[ci + 1] = Out()
                repl = textwrap.indent(
                    textwrap.dedent(
                        f"""\
                        import sys, tempfile
                        with tempfile.TemporaryDirectory() as out:
                            sys.argv = {["repro.py", *cmd]!r}
                            hl.main()
                        """
                    ),
                    "    ",
                )
                code = code.replace(main, repl)
                with open("repro.py", "w") as fd:
                    fd.write(code.lstrip())
                raise RuntimeError(f"wrote repro.py: {e}") from e
        raise

