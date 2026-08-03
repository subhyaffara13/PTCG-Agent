import subprocess

def launch(url: str, wait: bool = False, locate: bool = False) -> int:
    """This function launches the given URL (or filename) in the default
    viewer application for this file type.  If this is an executable, it
    might launch the executable in a new session.  The return value is
    the exit code of the launched application.  Usually, ``0`` indicates
    success.

    Examples::

        click.launch('https://click.palletsprojects.com/')
        click.launch('/my/downloaded/file', locate=True)

    .. versionadded:: 2.0

    :param url: URL or filename of the thing to launch.
    :param wait: Wait for the program to exit before returning. This
        only works if the launched program blocks. In particular,
        ``xdg-open`` on Linux does not block.
    :param locate: if this is set to `True` then instead of launching the
                   application associated with the URL it will attempt to
                   launch a file manager with the file located.  This
                   might have weird effects if the URL does not point to
                   the filesystem.
    """
    from ._termui_impl import open_url

    return open_url(url, wait=wait, locate=locate)


def launch(
    url: Annotated[
        str,
        Doc(
            """
            URL or filename of the thing to launch.
            """
        ),
    ],
    wait: Annotated[
        bool,
        Doc(
            """
            Wait for the program to exit before returning. This only works if the launched program blocks.
            In particular, `xdg-open` on Linux does not block.
            """
        ),
    ] = False,
    locate: Annotated[
        bool,
        Doc(
            """
            If this is set to `True`, then instead of launching the application associated with the URL, it will attempt to
            launch a file manager with the file located. This might have weird effects if the URL does not point to the filesystem.
            """
        ),
    ] = False,
) -> int:
    """
    This function launches the given URL (or filename) in the default
    viewer application for this file type.  If this is an executable, it
    might launch the executable in a new session.  The return value is
    the exit code of the launched application.  Usually, `0` indicates
    success.

    This function handles url in different operating systems separately:
     - On macOS (Darwin), it uses the `open` command.
     - On Linux and BSD, it uses `xdg-open` if available.
     - On Windows (and other OSes), it uses the standard webbrowser module.

    The function avoids, when possible, using the webbrowser module on Linux and macOS
    to prevent spammy terminal messages from some browsers (e.g., Chrome).

    ## Examples
    ```python
        import typer

        typer.launch("https://typer.tiangolo.com/")
    ```

    ```python
        import typer

        typer.launch("/my/downloaded/file", locate=True)
    ```
    """

    if url.startswith("http://") or url.startswith("https://"):
        if _is_macos():
            return subprocess.Popen(
                ["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ).wait()

        has_xdg_open = _is_linux_or_bsd() and shutil.which("xdg-open") is not None

        if has_xdg_open:
            return subprocess.Popen(
                ["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ).wait()

        import webbrowser

        webbrowser.open(url)

        return 0

    else:
        return click.launch(url, wait=wait, locate=locate)


def launch(args):
    if args.no_python and not args.use_env:
        raise ValueError(
            "When using the '--no-python' flag, you must also set the '--use-env' flag."
        )
    run(args)


def launch(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], grid_size_x: _ods_ir.Value[_ods_ir.IndexType], grid_size_y: _ods_ir.Value[_ods_ir.IndexType], grid_size_z: _ods_ir.Value[_ods_ir.IndexType], block_size_x: _ods_ir.Value[_ods_ir.IndexType], block_size_y: _ods_ir.Value[_ods_ir.IndexType], block_size_z: _ods_ir.Value[_ods_ir.IndexType], *, cluster_size_x: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, cluster_size_y: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, cluster_size_z: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, dynamic_shared_memory_size: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, cooperative: _Optional[bool] = None, module: _Optional[_Union[str, _ods_ir.FlatSymbolRefAttr]] = None, function: _Optional[_Union[str, _ods_ir.FlatSymbolRefAttr]] = None, workgroup_attributions: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, LaunchOp]:
  op = LaunchOp(asyncToken=async_token, asyncDependencies=async_dependencies, gridSizeX=grid_size_x, gridSizeY=grid_size_y, gridSizeZ=grid_size_z, blockSizeX=block_size_x, blockSizeY=block_size_y, blockSizeZ=block_size_z, clusterSizeX=cluster_size_x, clusterSizeY=cluster_size_y, clusterSizeZ=cluster_size_z, dynamicSharedMemorySize=dynamic_shared_memory_size, cooperative=cooperative, module=module, function=function, workgroup_attributions=workgroup_attributions, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

