import os
import subprocess

def check_msvc_cl_language_id(compiler: str) -> None:
    """
    Torch.compile() is only work on MSVC with English language pack well.
    Check MSVC's language pack: https://github.com/pytorch/pytorch/issues/157673#issuecomment-3051682766
    """

    def get_msvc_cl_path() -> tuple[bool, str]:
        """
        Finds the path to cl.exe using vswhere.exe.
        """
        vswhere_path = os.path.join(
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
            "Microsoft Visual Studio",
            "Installer",
            "vswhere.exe",
        )
        if not os.path.exists(vswhere_path):
            vswhere_path = os.path.join(
                os.environ.get("ProgramFiles", "C:\\Program Files"),
                "Microsoft Visual Studio",
                "Installer",
                "vswhere.exe",
            )
            if not os.path.exists(vswhere_path):
                return False, ""  # vswhere.exe not found

        try:
            # Get the Visual Studio installation path
            cmd = [
                vswhere_path,
                "-latest",
                "-prerelease",
                "-products",
                "*",
                "-requires",
                "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                "-property",
                "installationPath",
            ]
            vs_install_path = subprocess.check_output(
                cmd, text=True, encoding="utf-8"
            ).strip()

            if not vs_install_path:
                return False, ""

            # Find the latest MSVC toolset version within the installation
            msvc_tools_path = os.path.join(vs_install_path, "VC", "Tools", "MSVC")
            if not os.path.exists(msvc_tools_path):
                return False, ""

            # Get the latest toolset version directory
            toolset_versions = [
                d
                for d in os.listdir(msvc_tools_path)
                if os.path.isdir(os.path.join(msvc_tools_path, d))
            ]
            if not toolset_versions:
                return False, ""
            latest_toolset_version = sorted(toolset_versions, reverse=True)[0]

            # Construct the full cl.exe path
            cl_path = os.path.join(
                msvc_tools_path,
                latest_toolset_version,
                "bin",
                "HostX64",
                "x64",
                "cl.exe",
            )
            if os.path.exists(cl_path):
                return True, cl_path
            else:
                # Fallback for older versions or different architectures if needed
                cl_path = os.path.join(
                    msvc_tools_path,
                    latest_toolset_version,
                    "bin",
                    "HostX86",
                    "x86",
                    "cl.exe",
                )
                if os.path.exists(cl_path):
                    return True, cl_path

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, ""

        return False, ""

    if not _is_msvc_cl(compiler):
        return

    if os.path.exists(compiler):
        # Passed compiler with path.
        cl_exe_path = compiler
    else:
        b_ret, cl_exe_path = get_msvc_cl_path()
        if b_ret is False:
            return

    version_info = WinPeFileVersionInfo(cl_exe_path)
    lang_id = version_info.get_language_id()
    if lang_id != 1033:
        # MSVC English language id is 0x0409, and the DEC value is 1033.
        raise RuntimeError(
            "Torch.compile() is only support MSVC with English language pack,"
            "Please reinstall its language pack to English."
        )

