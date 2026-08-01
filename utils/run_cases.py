
def run_cases(cases, run_lambda, set_key):
    """Runs an array of cases and writes to file"""
    # Generate jobs to run from cases that do not have a result in
    # the previously loaded JSON.
    job_arg = [(case, run_lambda, set_key, index, len(cases))
               for index, case in enumerate(cases)
               if not result_exists(set_key, case)]

    print(f"{len(cases) - len(job_arg)}/{len(cases)} cases won't be "
          f"calculated because their results already exist.")

    jobs = []
    pool = Pool(num_pools)

    # Run all using multiprocess
    for case in job_arg:
        jobs.append(pool.apply_async(run, args=case, callback=write_result))

    pool.close()
    pool.join()

