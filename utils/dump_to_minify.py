import os
from typing import Any

def dump_to_minify(
    gm: torch.fx.GraphModule, args: Sequence[Any], compiler_name: str
) -> None:
    out = io.StringIO()
    # TODO: factor this out
    subdir = os.path.join(minifier_dir(), "checkpoints")
    if not os.path.exists(subdir):
        os.makedirs(subdir, exist_ok=True)
    save_graph_repro(out, gm, args, compiler_name, save_dir=subdir, command="minify")
    return helper_for_dump_minify(out.getvalue())


def dump_to_minify(
    exported_program: ExportedProgram,
    compiler_name: str,
    command: str = "minify",
    options: dict[str, Any] | None = None,
) -> None:
    """
    If command is "minify":
        Dump exported_program to `debug_dir/minifier/minifier_launcher.py`, with minify command.
    If command is "run":
        Dump exported_program to `cwd/repro.py`, with run command.
    """
    assert command in ["minify", "run"]

    subdir = os.path.join(minifier_dir(), "checkpoints")
    if not os.path.exists(subdir):
        os.makedirs(subdir, exist_ok=True)

    if command == "minify":
        out = io.StringIO()
        save_graph_repro_ep(
            out,
            compiler_name,
            exported_program=exported_program,
            save_dir=subdir,
            command="minify",
            config_patches=options,
        )
        return helper_for_dump_minify(out.getvalue())
    else:
        curdir = os.getcwd()
        file_name = os.path.join(curdir, "repro.py")
        try:
            with open(file_name, "w") as fd:
                save_graph_repro_ep(
                    fd,
                    compiler_name,
                    exported_program=exported_program,
                    config_patches=options,
                    save_dir=subdir,
                    command="run",
                    module_in_comment=True,
                )
            log.warning("Writing repro file to %s", file_name)
            if use_buck:
                BuckTargetWriter(file_name).write()
        except OSError:
            log.warning("No write permissions for %s", file_name)

