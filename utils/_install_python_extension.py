
def _install_python_extension(
    *, owner: str, repo_name: str, short_name: str, extension_dir: Path, branch: str
) -> ExtensionManifest:
    source_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/{branch}.zip"
    venv_dir = extension_dir / "venv"
    installed = False

    status = out.status()
    try:
        status.update(f"Creating virtual environment in {venv_dir}")
        if extension_dir.exists():
            shutil.rmtree(extension_dir, ignore_errors=True)
        extension_dir.mkdir(parents=True, exist_ok=False)

        uv_path = shutil.which("uv")
        venv_python = _get_venv_python_path(venv_dir)
        if uv_path:
            subprocess.run([uv_path, "venv", str(venv_dir)], check=True)
            status.done(f"Virtual environment created in {venv_dir}")

            status.update(f"Installing package from {source_url}")
            subprocess.run(
                [uv_path, "pip", "install", "--python", str(venv_python), source_url],
                check=True,
                timeout=_EXTENSIONS_PIP_INSTALL_TIMEOUT,
            )
        else:
            venv.EnvBuilder(with_pip=True).create(str(venv_dir))
            status.done(f"Virtual environment created in {venv_dir}")

            status.update(f"Installing package from {source_url}")
            subprocess.run(
                [
                    str(venv_python),
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    "--no-input",
                    source_url,
                ],
                check=True,
                timeout=_EXTENSIONS_PIP_INSTALL_TIMEOUT,
            )
        status.done(f"Package installed from {source_url}")

        executable_name = _get_executable_name(short_name)
        venv_executable = _get_venv_extension_executable_path(venv_dir, short_name)
        if not venv_executable.is_file():
            raise CLIError(
                f"Installed package from '{owner}/{repo_name}' does not expose the required console script "
                f"'{executable_name}'."
            )

        manifest = ExtensionManifest(
            owner=owner,
            repo=repo_name,
            repo_id=f"{owner}/{repo_name}",
            short_name=short_name,
            executable_name=executable_name,
            executable_path=str(venv_executable.resolve()),
            type="python",
            installed_at=datetime.now(timezone.utc),
            source=f"https://github.com/{owner}/{repo_name}",
        )
        installed = True
        return manifest
    except CLIError:
        raise
    except subprocess.TimeoutExpired as e:
        raise CLIExtensionInstallError(
            f"Pip install timed out after {_EXTENSIONS_PIP_INSTALL_TIMEOUT}s for '{owner}/{repo_name}'. "
            "See pip output above for details."
        ) from e
    except subprocess.CalledProcessError as e:
        raise CLIExtensionInstallError(
            f"Failed to install pip package from '{owner}/{repo_name}' (exit code {e.returncode}). "
            "See pip output above for details."
        ) from e
    except Exception as e:
        raise CLIExtensionInstallError(f"Failed to set up pip extension from '{owner}/{repo_name}': {e}") from e
    finally:
        if not installed:
            shutil.rmtree(extension_dir, ignore_errors=True)

