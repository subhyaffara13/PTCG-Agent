
def generate_standalone_repro(
    gm: torch.fx.GraphModule,
    args: Sequence[Any],
    *,
    save_path: str | None = None,
) -> str:
    """
    Generate a self-contained repro script from an FX graph.
    """
    buf = io.StringIO()
    save_graph_repro(buf, gm, args, "inductor", save_dir=None)
    repro = buf.getvalue()

    if save_path is not None:
        with open(save_path, "w") as f:
            f.write(repro)
        log.info("Saved standalone repro to %s", save_path)

    return repro

