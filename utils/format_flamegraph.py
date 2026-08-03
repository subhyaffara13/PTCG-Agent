import os
import subprocess

def format_flamegraph(flamegraph_lines, flamegraph_script=None):
    if flamegraph_script is None:
        cache_dir = os.path.expanduser("~/.cache/")
        os.makedirs(cache_dir, exist_ok=True)
        flamegraph_script = f"{cache_dir}/flamegraph.pl"
    if not os.path.exists(flamegraph_script):
        import tempfile
        import urllib.request

        print(f"Downloading flamegraph.pl to: {flamegraph_script}")
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pl") as f:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl",
                f.name,
            )
            try:
                os.chmod(f.name, 0o755)
                os.rename(f.name, flamegraph_script)
            except OSError:  # noqa: B001,E722
                # Ok to skip, the file will be removed by tempfile
                pass
    args = [flamegraph_script, "--countname", "bytes"]
    with subprocess.Popen(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8"
    ) as p:
        if p.stdin is None:
            raise AssertionError("p.stdin is None")
        if p.stdout is None:
            raise AssertionError("p.stdout is None")
        p.stdin.write(flamegraph_lines)
        p.stdin.close()
        result = p.stdout.read()
        p.stdout.close()
        p.wait()
        if p.wait() != 0:
            raise AssertionError(f"flamegraph process exited with code {p.wait()}")
        return result

