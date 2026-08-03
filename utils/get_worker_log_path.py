import os

def get_worker_log_path() -> str | None:
    log_loc = None
    if is_fbcode():
        mast_job_name = os.environ.get("MAST_HPC_JOB_NAME", None)
        global_rank = os.environ.get("ROLE_RANK", "0")

        if mast_job_name is not None:
            log_loc = f"/logs/dedicated_log_torch_compile_worker_rank{global_rank}"

    return log_loc

