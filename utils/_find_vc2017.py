
def _find_vc2017():
    """Returns "15, path" based on the result of invoking vswhere.exe
    If no install is found, returns "None, None"

    The version is returned to avoid unnecessarily changing the function
    result. It may be ignored when the path is not None.

    If vswhere.exe is not available, by definition, VS 2017 is not
    installed.
    """
    root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles")
    if not root:
        return None, None

    variant = 'arm64' if get_platform() == 'win-arm64' else 'x86.x64'
    suitable_components = (
        f"Microsoft.VisualStudio.Component.VC.Tools.{variant}",
        "Microsoft.VisualStudio.Workload.WDExpress",
    )

    for component in suitable_components:
        # Workaround for `-requiresAny` (only available on VS 2017 > 15.6)
        with contextlib.suppress(
            subprocess.CalledProcessError, OSError, UnicodeDecodeError
        ):
            path = (
                subprocess.check_output([
                    os.path.join(
                        root, "Microsoft Visual Studio", "Installer", "vswhere.exe"
                    ),
                    "-latest",
                    "-prerelease",
                    "-requires",
                    component,
                    "-property",
                    "installationPath",
                    "-products",
                    "*",
                ])
                .decode(encoding="mbcs", errors="strict")
                .strip()
            )

            path = os.path.join(path, "VC", "Auxiliary", "Build")
            if os.path.isdir(path):
                return 15, path

    return None, None  # no suitable component found

