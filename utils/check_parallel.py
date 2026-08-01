
def check_parallel(
    linter: PyLinter,
    jobs: int,
    files: Iterable[FileItem],
    extra_packages_paths: Sequence[str] | None = None,
) -> None:
    """Use the given linter to lint the files with given amount of workers (jobs).

    This splits the work filestream-by-filestream. If you need to do work across
    multiple files, as in the similarity-checker, then implement the map/reduce functionality.
    """
    # The linter is inherited by all the pool's workers, i.e. the linter
    # is identical to the linter object here. This is required so that
    # a custom PyLinter object can be used.
    initializer = functools.partial(
        _worker_initialize, extra_packages_paths=extra_packages_paths
    )
    with ProcessPoolExecutor(
        max_workers=jobs, initializer=initializer, initargs=(dill.dumps(linter),)
    ) as executor:
        linter.open()
        all_stats = []
        all_mapreduce_data: defaultdict[int, list[defaultdict[str, list[Any]]]] = (
            defaultdict(list)
        )

        # Maps each file to be worked on by a single _worker_check_single_file() call,
        # collecting any map/reduce data by checker module so that we can 'reduce' it
        # later.
        for (
            worker_idx,  # used to merge map/reduce data across workers
            module,
            file_path,
            base_name,
            messages,
            stats,
            msg_status,
            mapreduce_data,
        ) in executor.map(_worker_check_single_file, files):
            linter.file_state.base_name = base_name
            linter.file_state._is_base_filestate = False
            linter.set_current_module(module, file_path)
            for msg in messages:
                linter.reporter.handle_message(msg)
            all_stats.append(stats)
            all_mapreduce_data[worker_idx].append(mapreduce_data)
            linter.msg_status |= msg_status

    _merge_mapreduce_data(linter, all_mapreduce_data)
    linter.stats = merge_stats([linter.stats, *all_stats])

