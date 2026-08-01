
def _repos_callback(ctx: typer.Context) -> None:
    if ctx.info_name == "repo":
        out.warning("`hf repo` is deprecated in favor of `hf repos`.")

