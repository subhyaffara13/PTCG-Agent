
def _stream_logs_and_check_status(api: HfApi, job: JobInfo) -> None:
    """Stream Job logs until the Job ends, then fail the command if the Job did not complete successfully."""
    for log in api.fetch_job_logs(job_id=job.id, namespace=job.owner.name, follow=True):
        out.text(log)
    # The log stream can end while the Job is still scheduling or shutting down: settle the final state.
    final = api.wait_for_job(job_id=job.id, namespace=job.owner.name)
    if final.status.stage != JobStage.COMPLETED:
        message = f": {final.status.message}" if final.status.message else ""
        raise CLIError(f"Job {final.id} finished with stage '{final.status.stage}'{message}")
    out.text(f"Job {final.id} completed")

