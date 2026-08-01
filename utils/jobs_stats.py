
def jobs_stats(
    job_ids: JobIdsArg = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Fetch the resource usage statistics and metrics of Jobs"""
    if job_ids is not None:
        parsed_ids = []
        for job_id in job_ids:
            job_id, namespace = _parse_namespace_from_job_id(job_id, namespace)
            parsed_ids.append(job_id)
        job_ids = parsed_ids
    api = get_hf_api(token=token)
    if namespace is None:
        namespace = api.whoami()["name"]
    if job_ids is None:
        job_ids = [
            job.id
            for job in api.list_jobs(namespace=namespace)
            if (job.status.stage if job.status else "UNKNOWN") in ("RUNNING", "UPDATING")
        ]
    if len(job_ids) == 0:
        out.text("No running jobs found")
        return
    table_headers = [
        "JOB ID",
        "CPU %",
        "NUM CPU",
        "MEM %",
        "MEM USAGE",
        "NET I/O",
        "GPU UTIL %",
        "GPU MEM %",
        "GPU MEM USAGE",
    ]
    with multiprocessing.pool.ThreadPool(len(job_ids)) as pool:
        rows_per_job_id: dict[str, list[list[str | int]]] = {}
        for job_id in job_ids:
            row: list[str | int] = [job_id]
            row += ["-- / --" if ("/" in header or "USAGE" in header) else "--" for header in table_headers[1:]]
            rows_per_job_id[job_id] = [row]
        last_update_time = time.time()
        total_rows = [row for job_id in rows_per_job_id for row in rows_per_job_id[job_id]]
        # In-place refresh (cursor-up + clear) requires a fixed line count and layout —
        # `out.table`'s mode-dependent formatting would break it.
        print(_tabulate(total_rows, headers=table_headers))

        kwargs_list = [
            {
                "job_id": job_id,
                "metrics_stream": api.fetch_job_metrics(job_id=job_id, namespace=namespace),
                "table_headers": table_headers,
            }
            for job_id in job_ids
        ]
        for done, job_id, rows in iflatmap_unordered(pool, _get_jobs_stats_rows, kwargs_list=kwargs_list):
            if done:
                rows_per_job_id.pop(job_id, None)
            else:
                rows_per_job_id[job_id] = rows
            now = time.time()
            if now - last_update_time >= STATS_UPDATE_MIN_INTERVAL:
                _clear_line(2 + len(total_rows))
                total_rows = [row for job_id in rows_per_job_id for row in rows_per_job_id[job_id]]
                print(_tabulate(total_rows, headers=table_headers))
                last_update_time = now

