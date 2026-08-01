
def jobs_ps(
    all: Annotated[
        bool,
        typer.Option(
            "-a",
            "--all",
            help="Show all Jobs (default shows running and scheduling). Cannot be combined with --status.",
        ),
    ] = False,
    status: Annotated[
        list[str] | None,
        typer.Option(
            "--status",
            click_type=SoftChoice(JobStage),
            help="Only show Jobs with the given status. Comma-separated or repeated, e.g. `--status running,scheduling`.",
        ),
    ] = None,
    label: Annotated[
        list[str] | None,
        typer.Option(
            "-l",
            "--label",
            help="Only show Jobs with the given `key=value` label. Repeat to require several labels, e.g. `--label env=prod --label team=ml`.",
        ),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            help="Maximum number of Jobs to display. Set to 0 to show all (no limit).",
        ),
    ] = 100,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
    filter: Annotated[
        list[str] | None,
        typer.Option(
            "-f",
            "--filter",
            help="(Deprecated) Use `--status` and `--label` instead.",
        ),
    ] = None,
) -> None:
    """List Jobs.

    Use `--status` to filter by status (see [`JobStage`] for possible values) and `--label` to filter by `key=value`
    labels. A Job must match every filter to be listed.
    """
    api = get_hf_api(token=token)

    if filter:
        out.warning(
            f"Ignoring filter '{filter}'."
            " `-f`/`--filter` is deprecated and will be removed in a future release. Use `--status`/`--label`."
        )

    if all and status:
        raise CLIError("`-a`/`--all` cannot be combined with `--status`.")

    # Status filtering (default to active Jobs, unless `--all` or `--status` is provided).
    raw_statuses: list[str] = []
    for value in status or []:
        raw_statuses.extend(part.strip() for part in value.split(",") if part.strip())

    server_statuses: list[str] | None
    if raw_statuses:
        server_statuses = raw_statuses
    elif all:
        server_statuses = None
    else:
        server_statuses = [JobStage.RUNNING.value, JobStage.SCHEDULING.value]

    # Labels filtering
    labels: dict[str, str] = {}
    for item in label or []:
        if "=" not in item:
            raise CLIError(f"Invalid label filter '{item}': must be in the form 'key=value'")
        key, value = item.split("=")
        labels[key] = value

    jobs_iter = api.list_jobs(namespace=namespace, status=server_statuses, labels=labels or None)

    # Apply the display limit. Fetch one extra Job to detect (and warn about) truncation.
    truncated = False
    if limit > 0:
        jobs = list(itertools.islice(jobs_iter, limit + 1))
        if len(jobs) > limit:
            truncated = True
            jobs = jobs[:limit]
    else:
        jobs = list(jobs_iter)

    # Build display items. Augment the raw api dict with curated, table-friendly columns.
    job_items: list[dict[str, Any]] = []
    for job in jobs:
        job_item = _dataclass_to_dict(job)
        durations = job_item.get("durations") or {}
        cmd = job_item.get("command") or []
        job_item["job_id"] = job_item.get("id", "")
        job_item["image/space"] = job_item.get("docker_image") or "N/A"
        job_item["command"] = " ".join(cmd) if cmd else "N/A"
        job_item["created"] = job_item["created_at"][:19].replace("T", " ") if job_item.get("created_at") else "N/A"
        job_item["status"] = (job_item.get("status") or {}).get("stage", "UNKNOWN")
        job_item["runtime"] = format_duration(durations.get("running_secs"))
        job_items.append(job_item)

    out.table(
        job_items,
        headers=["job_id", "image/space", "command", "created", "status", "runtime"],
        id_key="job_id",
    )
    if truncated:
        out.hint(f"Output truncated to {limit} Jobs. Use `--limit 0` to show all (or `--limit N`).")
    if not job_items:
        if raw_statuses or labels:
            filters_msg = ", ".join(
                [*(f"status={s}" for s in raw_statuses), *(f"label={k}={v}" for k, v in labels.items())]
            )
            out.text(f"No jobs matched filters: {filters_msg}")
        elif not all:
            out.hint("No running jobs. Use `-a`/`--all` to include finished (and failed) jobs.")

