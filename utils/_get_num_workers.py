import os

def _get_num_workers(verbose: bool) -> int | None:
    max_jobs = os.environ.get('MAX_JOBS')
    if max_jobs is not None and max_jobs.isdigit():
        if verbose:
            logger.debug('Using envvar MAX_JOBS (%s) as the number of workers...', max_jobs)
        return int(max_jobs)
    if verbose:
        logger.info(
            'Allowing ninja to set a default number of workers... '
            '(overridable by setting the environment variable MAX_JOBS=N)'
        )
    return None

