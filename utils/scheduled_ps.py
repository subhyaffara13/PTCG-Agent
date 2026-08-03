from typing import Any

def scheduled_ps(
    all: Annotated[
        bool,
        typer.Option(
            "-a",
            "--all",
            help="Show all scheduled Jobs (default hides suspended)",
        ),
    ] = False,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
    filter: Annotated[
        list[str] | None,
        typer.Option(
            "-f",
            "--filter",
            help="Filter output based on conditions provided (format: key=value)",
        ),
    ] = None,
) -> None:
    """List scheduled Jobs"""
    api = get_hf_api(token=token)
    scheduled_jobs = api.list_scheduled_jobs(namespace=namespace)
    filters: list[tuple[str, str, str]] = []
    for f in filter or []:
        if "=" in f:
            key, value = f.split("=", 1)
            # Negate predicate in case of key!=value
            if key.endswith("!"):
                op = "!="
                key = key[:-1]
            else:
                op = "="
            filters.append((key.lower(), op, value.lower()))
        else:
            out.warning(f"Ignoring invalid filter format '{f}'. Use key=value format.")

    # Filter scheduled jobs (operating on ScheduledJobInfo objects to preserve existing filter behavior)
    filtered_jobs = []
    for scheduled_job in scheduled_jobs:
        suspend = scheduled_job.suspend or False
        if not all and suspend:
            continue
        image_or_space = scheduled_job.job_spec.docker_image or "N/A"
        cmd = scheduled_job.job_spec.command or []
        command_str = " ".join(cmd) if cmd else "N/A"
        props = {"id": scheduled_job.id, "image": image_or_space, "suspend": str(suspend), "command": command_str}
        if not _matches_filters(props, filters):
            continue
        filtered_jobs.append(scheduled_job)

    # Build display items. Augment with curated columns.
    items: list[dict[str, Any]] = []
    for sj in filtered_jobs:
        item = _dataclass_to_dict(sj)
        job_spec = item.get("job_spec") or {}
        status_dict = item.get("status") or {}
        last_job = status_dict.get("last_job")
        cmd = job_spec.get("command") or []
        item["image/space"] = job_spec.get("docker_image") or "N/A"
        item["command"] = " ".join(cmd) if cmd else "N/A"
        item["last_run"] = last_job["at"][:19].replace("T", " ") if last_job and last_job.get("at") else "N/A"
        item["next_run"] = (
            status_dict["next_job_run_at"][:19].replace("T", " ") if status_dict.get("next_job_run_at") else "N/A"
        )
        item["suspend"] = item.get("suspend") or False
        items.append(item)

    out.table(
        items,
        headers=["id", "schedule", "image/space", "command", "last_run", "next_run", "suspend"],
        id_key="id",
    )
    if not items and filters:
        filters_msg = ", ".join(f"{k}{o}{v}" for k, o, v in filters)
        out.text(f"No scheduled jobs matched filters: {filters_msg}")

