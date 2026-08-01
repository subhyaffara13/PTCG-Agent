
def _determine_next_job(status: LargeUploadStatus) -> tuple[WorkerJob, list[JOB_ITEM_T]] | None:
    with status.lock:
        # 1. Commit if more than 5 minutes since last commit attempt (and at least 1 file)
        if (
            status.nb_workers_commit == 0
            and status.queue_commit.qsize() > 0
            and status.last_commit_attempt is not None
            and time.time() - status.last_commit_attempt > 5 * 60
        ):
            status.nb_workers_commit += 1
            logger.debug("Job: commit (more than 5 minutes since last commit attempt)")
            return (WorkerJob.COMMIT, _get_n(status.queue_commit, status.target_chunk()))

        # 2. Commit if at least 100 files are ready to commit
        elif status.nb_workers_commit == 0 and status.queue_commit.qsize() >= 150:
            status.nb_workers_commit += 1
            logger.debug("Job: commit (>100 files ready)")
            return (WorkerJob.COMMIT, _get_n(status.queue_commit, status.target_chunk()))

        # 3. Get upload mode if at least 100 files
        elif status.queue_get_upload_mode.qsize() >= MAX_NB_FILES_FETCH_UPLOAD_MODE:
            status.nb_workers_get_upload_mode += 1
            logger.debug(f"Job: get upload mode (>{MAX_NB_FILES_FETCH_UPLOAD_MODE} files ready)")
            return (WorkerJob.GET_UPLOAD_MODE, _get_n(status.queue_get_upload_mode, MAX_NB_FILES_FETCH_UPLOAD_MODE))

        # 4. Preupload LFS file if at least `status.upload_batch_size` files and no worker is preuploading LFS
        elif status.queue_preupload_lfs.qsize() >= status.upload_batch_size and status.nb_workers_preupload_lfs == 0:
            status.nb_workers_preupload_lfs += 1
            logger.debug("Job: preupload LFS (no other worker preuploading LFS)")
            return (WorkerJob.PREUPLOAD_LFS, _get_n(status.queue_preupload_lfs, status.upload_batch_size))

        # 5. Compute sha256 if at least 1 file and no worker is computing sha256
        elif status.queue_sha256.qsize() > 0 and status.nb_workers_sha256 == 0:
            status.nb_workers_sha256 += 1
            logger.debug("Job: sha256 (no other worker computing sha256)")
            return (WorkerJob.SHA256, _get_one(status.queue_sha256))

        # 6. Get upload mode if at least 1 file and no worker is getting upload mode
        elif status.queue_get_upload_mode.qsize() > 0 and status.nb_workers_get_upload_mode == 0:
            status.nb_workers_get_upload_mode += 1
            logger.debug("Job: get upload mode (no other worker getting upload mode)")
            return (WorkerJob.GET_UPLOAD_MODE, _get_n(status.queue_get_upload_mode, MAX_NB_FILES_FETCH_UPLOAD_MODE))

        # 7. Preupload LFS file if at least `status.upload_batch_size` files
        elif status.queue_preupload_lfs.qsize() >= status.upload_batch_size:
            status.nb_workers_preupload_lfs += 1
            logger.debug("Job: preupload LFS")
            return (WorkerJob.PREUPLOAD_LFS, _get_n(status.queue_preupload_lfs, status.upload_batch_size))

        # 8. Compute sha256 if at least 1 file
        elif status.queue_sha256.qsize() > 0:
            status.nb_workers_sha256 += 1
            logger.debug("Job: sha256")
            return (WorkerJob.SHA256, _get_one(status.queue_sha256))

        # 9. Get upload mode if at least 1 file
        elif status.queue_get_upload_mode.qsize() > 0:
            status.nb_workers_get_upload_mode += 1
            logger.debug("Job: get upload mode")
            return (WorkerJob.GET_UPLOAD_MODE, _get_n(status.queue_get_upload_mode, MAX_NB_FILES_FETCH_UPLOAD_MODE))

        # 10. Preupload LFS file if at least 1 file
        elif status.queue_preupload_lfs.qsize() > 0:
            status.nb_workers_preupload_lfs += 1
            logger.debug("Job: preupload LFS")
            return (WorkerJob.PREUPLOAD_LFS, _get_n(status.queue_preupload_lfs, status.upload_batch_size))

        # 11. Commit if at least 1 file and 1 min since last commit attempt
        elif (
            status.nb_workers_commit == 0
            and status.queue_commit.qsize() > 0
            and status.last_commit_attempt is not None
            and time.time() - status.last_commit_attempt > 1 * 60
        ):
            status.nb_workers_commit += 1
            logger.debug("Job: commit (1 min since last commit attempt)")
            return (WorkerJob.COMMIT, _get_n(status.queue_commit, status.target_chunk()))

        # 12. Commit if at least 1 file all other queues are empty and all workers are waiting
        #     e.g. when it's the last commit
        elif (
            status.nb_workers_commit == 0
            and status.queue_commit.qsize() > 0
            and status.queue_sha256.qsize() == 0
            and status.queue_get_upload_mode.qsize() == 0
            and status.queue_preupload_lfs.qsize() == 0
            and status.nb_workers_sha256 == 0
            and status.nb_workers_get_upload_mode == 0
            and status.nb_workers_preupload_lfs == 0
        ):
            status.nb_workers_commit += 1
            logger.debug("Job: commit")
            return (WorkerJob.COMMIT, _get_n(status.queue_commit, status.target_chunk()))

        # 13. If all queues are empty, exit
        elif all(metadata.is_committed or metadata.should_ignore for _, metadata in status.items):
            logger.info("All files have been processed! Exiting worker.")
            return None

        # 14. If no task is available, wait
        else:
            status.nb_workers_waiting += 1
            logger.debug(f"No task available, waiting... ({WAITING_TIME_IF_NO_TASKS}s)")
            return (WorkerJob.WAIT, [])

