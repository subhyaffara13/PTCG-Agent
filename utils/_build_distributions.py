import subprocess
import sys
from pathlib import Path


def _build_distributions(tmp_path_factory, request):
    with contexts.session_locked_tmp_dir(
        request, tmp_path_factory, "dist_build"
    ) as tmp:  # pragma: no cover
        sdist = next(tmp.glob("*.tar.gz"), None)
        wheel = next(tmp.glob("*.whl"), None)
        if sdist and wheel:
            return (sdist, wheel)

        # Sanity check: should not create recursive setuptools/build/lib/build/lib/...
        assert not Path(request.config.rootdir, "build/lib/build").exists()

        subprocess.check_output([
            sys.executable,
            "-m",
            "build",
            "--outdir",
            str(tmp),
            str(request.config.rootdir),
        ])

        # Sanity check: should not create recursive setuptools/build/lib/build/lib/...
        assert not Path(request.config.rootdir, "build/lib/build").exists()

        return next(tmp.glob("*.tar.gz")), next(tmp.glob("*.whl"))

