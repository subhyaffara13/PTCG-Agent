import time

def _worker_job(
    status: LargeUploadStatus,
    api: "HfApi",
    repo_id: str,
    repo_type: str,
    revision: str,
):
    """
    Main process for a worker. The worker will perform tasks based on the priority list until all files are uploaded
    and committed. If no tasks are available, the worker will wait for 10 seconds before checking again.

    If a task fails for any reason, the item(s) are put back in the queue for another worker to pick up.

    Read `upload_large_folder` docstring for more information on how tasks are prioritized.
    """
    while True:
        next_job: tuple[WorkerJob, list[JOB_ITEM_T]] | None = None

        # Determine next task
        next_job = _determine_next_job(status)
        if next_job is None:
            return
        job, items = next_job

        # Perform task
        match job:
            case WorkerJob.SHA256:
                item = items[0]  # single item
                try:
                    _compute_sha256(item)
                    status.queue_get_upload_mode.put(item)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"Failed to compute sha256: {e}")
                    traceback.format_exc()
                    status.queue_sha256.put(item)

                with status.lock:
                    status.nb_workers_sha256 -= 1

            case WorkerJob.GET_UPLOAD_MODE:
                try:
                    _get_upload_mode(items, api=api, repo_id=repo_id, repo_type=repo_type, revision=revision)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"Failed to get upload mode: {e}")
                    traceback.format_exc()

                # Items are either:
                # - dropped (if should_ignore)
                # - put in LFS queue (if LFS)
                # - put in commit queue (if regular)
                # - or put back (if error occurred).
                for item in items:
                    _, metadata = item
                    if metadata.should_ignore:
                        continue
                    match metadata.upload_mode:
                        case "lfs":
                            status.queue_preupload_lfs.put(item)
                        case "regular":
                            status.queue_commit.put(item)
                        case _:
                            status.queue_get_upload_mode.put(item)

                with status.lock:
                    status.nb_workers_get_upload_mode -= 1

            case WorkerJob.PREUPLOAD_LFS:
                try:
                    _preupload_lfs(items, api=api, repo_id=repo_id, repo_type=repo_type, revision=revision)
                    for item in items:
                        status.queue_commit.put(item)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"Failed to preupload LFS: {e}")
                    traceback.format_exc()
                    for item in items:
                        status.queue_preupload_lfs.put(item)

                with status.lock:
                    status.nb_workers_preupload_lfs -= 1

            case WorkerJob.COMMIT:
                start_ts = time.time()
                success = True
                try:
                    _commit(items, api=api, repo_id=repo_id, repo_type=repo_type, revision=revision)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"Failed to commit: {e}")
                    traceback.format_exc()
                    for item in items:
                        status.queue_commit.put(item)
                    success = False
                duration = time.time() - start_ts
                status.update_chunk(success, len(items), duration)
                with status.lock:
                    status.last_commit_attempt = time.time()
                    status.nb_workers_commit -= 1

            case WorkerJob.WAIT:
                time.sleep(WAITING_TIME_IF_NO_TASKS)
                with status.lock:
                    status.nb_workers_waiting -= 1

