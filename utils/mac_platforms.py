import subprocess
import sys
from typing import Optional

def mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for macOS.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.

    :param tuple version: A two-item tuple representing the version of macOS.
                          Defaults to the current system's version.
    :param str arch: The CPU architecture. Defaults to the architecture of the
                     current system, e.g. ``"x86_64"``.

    .. note::
        Equivalent support for the other major platforms is purposefully not
        provided:

        - On Windows, platform compatibility is statically specified
        - On Linux, code must be run on the system itself to determine
          compatibility
    """
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))
        if version == (10, 16):
            # When built against an older macOS SDK, Python will report macOS 10.16
            # instead of the real version.
            version_str = subprocess.run(
                [
                    sys.executable,
                    "-sS",
                    "-c",
                    "import platform; print(platform.mac_ver()[0])",
                ],
                check=True,
                env={"SYSTEM_VERSION_COMPAT": "0"},
                stdout=subprocess.PIPE,
                text=True,
            ).stdout
            version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))

    if arch is None:
        arch = _mac_arch(cpu_arch)

    if (10, 0) <= version < (11, 0):
        # Prior to Mac OS 11, each yearly release of Mac OS bumped the
        # "minor" version number.  The major version was always 10.
        major_version = 10
        for minor_version in range(version[1], -1, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Starting with Mac OS 11, each yearly release bumps the major version
        # number.   The minor versions are now the midyear updates.
        minor_version = 0
        for major_version in range(version[0], 10, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Mac OS 11 on x86_64 is compatible with binaries from previous releases.
        # Arm64 support was introduced in 11.0, so no Arm binaries from previous
        # releases exist.
        #
        # However, the "universal2" binary format can have a
        # macOS version earlier than 11.0 when the x86_64 part of the binary supports
        # that version of macOS.
        major_version = 10
        if arch == "x86_64":
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield f"macosx_{major_version}_{minor_version}_{binary_format}"
        else:
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_format = "universal2"
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"


def mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
) -> Iterator[str]:
    """
    Yields the platform tags for a macOS system.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.
    """
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))
        if version == (10, 16):
            # When built against an older macOS SDK, Python will report macOS 10.16
            # instead of the real version.
            version_str = subprocess.run(
                [
                    sys.executable,
                    "-sS",
                    "-c",
                    "import platform; print(platform.mac_ver()[0])",
                ],
                check=True,
                env={"SYSTEM_VERSION_COMPAT": "0"},
                stdout=subprocess.PIPE,
                text=True,
            ).stdout
            version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))

    if arch is None:
        arch = _mac_arch(cpu_arch)

    if (10, 0) <= version < (11, 0):
        # Prior to Mac OS 11, each yearly release of Mac OS bumped the
        # "minor" version number.  The major version was always 10.
        major_version = 10
        for minor_version in range(version[1], -1, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Starting with Mac OS 11, each yearly release bumps the major version
        # number.   The minor versions are now the midyear updates.
        minor_version = 0
        for major_version in range(version[0], 10, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Mac OS 11 on x86_64 is compatible with binaries from previous releases.
        # Arm64 support was introduced in 11.0, so no Arm binaries from previous
        # releases exist.
        #
        # However, the "universal2" binary format can have a
        # macOS version earlier than 11.0 when the x86_64 part of the binary supports
        # that version of macOS.
        major_version = 10
        if arch == "x86_64":
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield f"macosx_{major_version}_{minor_version}_{binary_format}"
        else:
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_format = "universal2"
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"


def mac_platforms(
    version: Optional[MacVersion] = None, arch: Optional[str] = None
) -> Iterator[str]:
    """
    Yields the platform tags for a macOS system.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.
    """
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = cast("MacVersion", tuple(map(int, version_str.split(".")[:2])))
    else:
        version = version
    if arch is None:
        arch = _mac_arch(cpu_arch)
    else:
        arch = arch

    if (10, 0) <= version and version < (11, 0):
        # Prior to Mac OS 11, each yearly release of Mac OS bumped the
        # "minor" version number.  The major version was always 10.
        for minor_version in range(version[1], -1, -1):
            compat_version = 10, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=10, minor=minor_version, binary_format=binary_format
                )

    if version >= (11, 0):
        # Starting with Mac OS 11, each yearly release bumps the major version
        # number.   The minor versions are now the midyear updates.
        for major_version in range(version[0], 10, -1):
            compat_version = major_version, 0
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=major_version, minor=0, binary_format=binary_format
                )

    if version >= (11, 0):
        # Mac OS 11 on x86_64 is compatible with binaries from previous releases.
        # Arm64 support was introduced in 11.0, so no Arm binaries from previous
        # releases exist.
        #
        # However, the "universal2" binary format can have a
        # macOS version earlier than 11.0 when the x86_64 part of the binary supports
        # that version of macOS.
        if arch == "x86_64":
            for minor_version in range(16, 3, -1):
                compat_version = 10, minor_version
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield "macosx_{major}_{minor}_{binary_format}".format(
                        major=compat_version[0],
                        minor=compat_version[1],
                        binary_format=binary_format,
                    )
        else:
            for minor_version in range(16, 3, -1):
                compat_version = 10, minor_version
                binary_format = "universal2"
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=compat_version[0],
                    minor=compat_version[1],
                    binary_format=binary_format,
                )


def mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for macOS.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.

    :param tuple version: A two-item tuple representing the version of macOS.
                          Defaults to the current system's version.
    :param str arch: The CPU architecture. Defaults to the architecture of the
                     current system, e.g. ``"x86_64"``.

    .. note::
        Equivalent support for the other major platforms is purposefully not
        provided:

        - On Windows, platform compatibility is statically specified
        - On Linux, code must be run on the system itself to determine
          compatibility
    """
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))
        if version == (10, 16):
            # When built against an older macOS SDK, Python will report macOS 10.16
            # instead of the real version.
            version_str = subprocess.run(
                [
                    sys.executable,
                    "-sS",
                    "-c",
                    "import platform; print(platform.mac_ver()[0])",
                ],
                check=True,
                env={"SYSTEM_VERSION_COMPAT": "0"},
                stdout=subprocess.PIPE,
                text=True,
            ).stdout
            version = cast("AppleVersion", tuple(map(int, version_str.split(".")[:2])))

    if arch is None:
        arch = _mac_arch(cpu_arch)

    if (10, 0) <= version < (11, 0):
        # Prior to Mac OS 11, each yearly release of Mac OS bumped the
        # "minor" version number.  The major version was always 10.
        major_version = 10
        for minor_version in range(version[1], -1, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Starting with Mac OS 11, each yearly release bumps the major version
        # number.   The minor versions are now the midyear updates.
        minor_version = 0
        for major_version in range(version[0], 10, -1):
            compat_version = major_version, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

    if version >= (11, 0):
        # Mac OS 11 on x86_64 is compatible with binaries from previous releases.
        # Arm64 support was introduced in 11.0, so no Arm binaries from previous
        # releases exist.
        #
        # However, the "universal2" binary format can have a
        # macOS version earlier than 11.0 when the x86_64 part of the binary supports
        # that version of macOS.
        major_version = 10
        if arch == "x86_64":
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield f"macosx_{major_version}_{minor_version}_{binary_format}"
        else:
            for minor_version in range(16, 3, -1):
                compat_version = major_version, minor_version
                binary_format = "universal2"
                yield f"macosx_{major_version}_{minor_version}_{binary_format}"

