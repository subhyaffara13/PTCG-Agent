import time

def _spaces_hot_reload_summary(
    api: HfApi,
    space_id: str,
    current_sha: str | None,
    commit_sha: str,
    filename: str,
    local_path: str,
    token: str | None,
) -> None:
    while (space_info := api.space_info(space_id)).sha == current_sha:
        if current_sha is None or current_sha == commit_sha:
            break
        typer.secho("Waiting for up-to-date Space infos", fg=typer.colors.BRIGHT_BLACK, err=True)
        time.sleep(2)
    if space_info.sha != commit_sha:
        raise CLIError(f"Expected SHA {commit_sha} after hot-reload but got {space_info.sha}")
    if (runtime := space_info.runtime) is None:
        raise CLIError(f"Unable to read SpaceRuntime from {space_id} infos")
    if (hot_reloading := runtime.hot_reloading) is None:
        raise CLIError(f"Space {space_id} current running version has not been hot-reloaded")
    if hot_reloading.status != "created":
        typer.echo(f"Failed creating hot-reloaded commit. {hot_reloading.replica_statuses=}")
        return

    if (space_host := space_info.host) is None:
        raise CLIError("Unexpected None host on hotReloaded Space")
    if (space_subdomain := space_info.subdomain) is None:
        raise CLIError("Unexpected None subdomain on hotReloaded Space")

    def render_region(region: ReloadRegion) -> str:
        res = f"{local_path}, "
        if region["startLine"] == region["endLine"]:
            res += f"line {region['startLine'] - 1}"
        else:
            res += f"lines {region['startLine'] - 1}-{region['endLine']}"
        return res

    def display_event(event: ApiGetReloadEventSourceData) -> None:
        if event["data"]["kind"] == "error":
            typer.secho("✘ Unexpected hot-reloading error", bold=True)
            typer.secho(event["data"]["traceback"], italic=True)
        elif event["data"]["kind"] == "exception":
            typer.secho(f"✘ Exception at {render_region(event['data']['region'])}", bold=True)
            typer.secho(event["data"]["traceback"], italic=True)
        elif event["data"]["kind"] == "add":
            typer.secho(f"✔︎ Created {event['data']['objectName']} {event['data']['objectType']}", bold=True)
        elif event["data"]["kind"] == "delete":
            typer.secho(f"∅ Deleted {event['data']['objectName']} {event['data']['objectType']}", bold=True)
        elif event["data"]["kind"] == "update":
            typer.secho(f"✔︎ Updated {event['data']['objectName']} {event['data']['objectType']}", bold=True)
        elif event["data"]["kind"] == "run":
            typer.secho(f"▶ Run {render_region(event['data']['region'])}", bold=True)
            typer.secho(event["data"]["codeLines"], italic=True)
        elif event["data"]["kind"] == "ui":
            if event["data"]["updated"]:
                typer.secho("⟳ UI updated", bold=True)
            else:
                typer.secho("∅ UI untouched", bold=True)
        elif event["data"]["kind"] == "file":
            if event["data"]["created"]:
                typer.secho(f"✔︎ {filename} created", bold=True)
            else:
                typer.secho(f"✔︎ {filename} updated", bold=True)
        else:
            typer.secho(f"❓ Unknown update event: {event=}")
            if TYPE_CHECKING:
                assert_never(event["data"]["kind"])

    for replica_stream_event in multi_replica_reload_events(
        commit_sha=commit_sha,
        host=space_host,
        subdomain=space_subdomain,
        replica_hashes=[hash for hash, _ in hot_reloading.replica_statuses],
        token=token,
    ):
        if replica_stream_event["kind"] == "event":
            display_event(replica_stream_event["event"])
        elif replica_stream_event["kind"] == "replicaHash":
            typer.secho(f"---- Replica {replica_stream_event['hash']} ----")
        elif replica_stream_event["kind"] == "fullMatch":
            typer.echo("✔︎ Same as first replica")
        elif replica_stream_event["kind"] == "warning":
            typer.secho(f"⚠ {replica_stream_event['message']}", fg=typer.colors.BRIGHT_BLACK)
        else:
            assert_never(replica_stream_event)

