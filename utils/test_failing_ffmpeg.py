import os
import subprocess

def test_failing_ffmpeg(tmp_path, monkeypatch, anim):
    """
    Test that we correctly raise a CalledProcessError when ffmpeg fails.

    To do so, mock ffmpeg using a simple executable shell script that
    succeeds when called with no arguments (so that it gets registered by
    `isAvailable`), but fails otherwise, and add it to the $PATH.
    """
    monkeypatch.setenv("PATH", str(tmp_path), prepend=":")
    exe_path = tmp_path / "ffmpeg"
    exe_path.write_bytes(b"#!/bin/sh\n[[ $@ -eq 0 ]]\n")
    os.chmod(exe_path, 0o755)
    with pytest.raises(subprocess.CalledProcessError):
        anim.save("test.mpeg")

