import os
import subprocess

def _get_vc_env(vc_arch: str) -> dict[str, str]:
    try:
        from setuptools import distutils  # type: ignore[attr-defined]

        return distutils._msvccompiler._get_vc_env(vc_arch)
    except AttributeError:
        try:
            from setuptools._distutils import _msvccompiler
            return _msvccompiler._get_vc_env(vc_arch)  # type: ignore[attr-defined]
        except AttributeError:
            from setuptools._distutils.compilers.C import msvc
            return msvc._get_vc_env(vc_arch)  # type: ignore[attr-defined]


def _get_vc_env(plat_spec):
    if os.getenv("DISTUTILS_USE_SDK"):
        return {key.lower(): value for key, value in os.environ.items()}

    vcvarsall, _ = _find_vcvarsall(plat_spec)
    if not vcvarsall:
        raise DistutilsPlatformError(
            'Microsoft Visual C++ 14.0 or greater is required. '
            'Get it with "Microsoft C++ Build Tools": '
            'https://visualstudio.microsoft.com/visual-cpp-build-tools/'
        )

    try:
        out = subprocess.check_output(
            f'cmd /u /c "{vcvarsall}" {plat_spec} && set',
            stderr=subprocess.STDOUT,
        ).decode('utf-16le', errors='replace')
    except subprocess.CalledProcessError as exc:
        log.error(exc.output)
        raise DistutilsPlatformError(f"Error executing {exc.cmd}")

    env = {
        key.lower(): value
        for key, _, value in (line.partition('=') for line in out.splitlines())
        if key and value
    }

    return env

