
def _create_job_spec(
    *,
    image: str,
    command: list[str],
    env: dict[str, Any] | None,
    secrets: dict[str, Any] | None,
    flavor: JobHardware | str | None,
    timeout: int | float | str | None,
    labels: dict[str, str] | None = None,
    volumes: list[Volume] | None = None,
    expose: list[int] | None = None,
    ssh: bool = False,
) -> dict[str, Any]:
    # prepare job spec to send to HF Jobs API
    job_spec: dict[str, Any] = {
        "command": command,
        "arguments": [],
        "environment": env or {},
        "flavor": flavor or JobHardware.CPU_BASIC,
    }
    # secrets are optional
    if secrets:
        job_spec["secrets"] = secrets
    # timeout is optional
    if timeout:
        time_units_factors = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
        if isinstance(timeout, str) and timeout[-1] in time_units_factors:
            job_spec["timeoutSeconds"] = int(float(timeout[:-1]) * time_units_factors[timeout[-1]])
        else:
            job_spec["timeoutSeconds"] = int(timeout)
    # labels are optional
    if labels:
        job_spec["labels"] = labels
    # volumes are optional
    if volumes:
        job_spec["volumes"] = [vol.to_dict() for vol in volumes]
    # expose ports through the jobs proxy
    if expose:
        job_spec["expose"] = {"ports": expose}
    # make the job container reachable over SSH
    if ssh:
        job_spec["ssh"] = {"enabled": True}
    # input is either from docker hub or from HF spaces
    for prefix in (
        "https://huggingface.co/spaces/",
        "https://hf.co/spaces/",
        "huggingface.co/spaces/",
        "hf.co/spaces/",
    ):
        if image.startswith(prefix):
            job_spec["spaceId"] = image[len(prefix) :]
            break
    else:
        job_spec["dockerImage"] = image
    return job_spec

