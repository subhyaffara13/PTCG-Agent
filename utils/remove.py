import os

def remove(path):
  """Remove the file at path. Might fail if used on a directory path."""
  if io_mode == BackendMode.DEFAULT:
    return os.remove(path)
  elif io_mode == BackendMode.TF:
    return gfile.remove(path)
  else:
    raise ValueError('Unknown IO Backend Mode.')


def remove(predicate, seq):
    """ Return those items of sequence for which predicate(item) is False

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(remove(iseven, [1, 2, 3, 4]))
    [1, 3]
    """
    return filterfalse(predicate, seq)


def remove(module, name):
    r"""Remove the pruning reparameterization from a module and the pruning method from the forward hook.

    The pruned parameter named ``name`` remains permanently pruned, and the parameter
    named ``name+'_orig'`` is removed from the parameter list. Similarly,
    the buffer named ``name+'_mask'`` is removed from the buffers.

    Note:
        Pruning itself is NOT undone or reversed!

    Args:
        module (nn.Module): module containing the tensor to prune
        name (str): parameter name within ``module`` on which pruning
            will act.

    Examples:
        >>> m = random_unstructured(nn.Linear(5, 7), name="weight", amount=0.2)
        >>> m = remove(m, name="weight")
    """
    for k, hook in module._forward_pre_hooks.items():
        if isinstance(hook, BasePruningMethod) and hook._tensor_name == name:
            hook.remove(module)
            del module._forward_pre_hooks[k]
            return module

    raise ValueError(
        f"Parameter '{name}' of module {module} has to be pruned before pruning can be removed"
    )


def remove(x, f):
    if f < 2:
        raise ValueError("factor must be > 1")
    if x == 0:
        return 0, 0
    if f == 2:
        b = bit_scan1(x)
        return x >> b, b
    m = 0
    y, rem = divmod(x, f)
    while not rem:
        x = y
        m += 1
        if m > 5:
            pow_list = [f**2]
            while pow_list:
                _f = pow_list[-1]
                y, rem = divmod(x, _f)
                if not rem:
                    m += 1 << len(pow_list)
                    x = y
                    pow_list.append(_f**2)
                else:
                    pow_list.pop()
        y, rem = divmod(x, f)
    return x, m


def remove(
    argument: Annotated[
        str,
        typer.Argument(
            help=(
                "Bucket path: namespace/bucket_name/path or hf://buckets/namespace/bucket_name/path."
                " With --recursive, namespace/bucket_name is also accepted to target all files."
            ),
        ),
    ],
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-R",
            help="Remove files recursively under the given prefix.",
        ),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Skip confirmation prompt.",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Preview what would be deleted without actually deleting.",
        ),
    ] = False,
    include: Annotated[
        list[str] | None,
        typer.Option(
            help="Include only files matching pattern (can specify multiple). Requires --recursive.",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            help="Exclude files matching pattern (can specify multiple). Requires --recursive.",
        ),
    ] = None,
    token: TokenOpt = None,
) -> None:
    """Remove files from a bucket.

    To delete an entire bucket, use `hf buckets delete` instead.
    """
    parsed = _parse_bucket_uri(argument)
    bucket_id = parsed.id
    prefix = parsed.path_in_repo

    if prefix == "" and not recursive:
        raise typer.BadParameter(
            f"No file path specified. To remove files, provide a path"
            f" (e.g. '{bucket_id}/FILE') or use --recursive to remove all files."
            f" To delete the entire bucket, use `hf buckets delete {bucket_id}`."
        )

    if (include or exclude) and not recursive:
        raise typer.BadParameter("--include and --exclude require --recursive.")

    api = get_hf_api(token=token)

    if recursive:
        status = out.status("Listing files from remote")

        all_files: list[BucketFile] = []
        for item in api.list_bucket_tree(
            bucket_id,
            prefix=prefix or None,
            recursive=True,
        ):
            if isinstance(item, BucketFile):
                all_files.append(item)
                status.update(f"Listing files from remote ({len(all_files)} files)")
        status.done(f"Listing files from remote ({len(all_files)} files)")

        if include or exclude:
            matcher = FilterMatcher(include_patterns=include, exclude_patterns=exclude)
            matched_files = [f for f in all_files if matcher.matches(f.path)]
        else:
            matched_files = all_files

        file_paths = [f.path for f in matched_files]
        total_size = sum(f.size for f in matched_files)
        size_str = format_size(total_size, human_readable=True)

        if not file_paths:
            out.text("No files to remove.")
            return

        count_label = f"{len(file_paths)} file(s) totaling {size_str}"

        if not yes and not dry_run:
            out.text("\n".join(f"  {path}" for path in file_paths))
            out.confirm(f"Remove {count_label} from '{bucket_id}'?", yes=False)

        if dry_run:
            out.text("\n".join(f"delete: {BUCKET_PREFIX}{bucket_id}/{path}" for path in file_paths))
            out.text(f"(dry run) {count_label} would be removed.")
            return

        api.batch_bucket_files(bucket_id, delete=file_paths)
        out.result(
            f"Removed {count_label} from '{bucket_id}'",
            bucket_id=bucket_id,
            files_deleted=len(file_paths),
            size=size_str,
        )

    else:
        file_path = prefix
        if not file_path:
            raise typer.BadParameter("File path cannot be empty.")

        if dry_run:
            out.text(f"delete: {BUCKET_PREFIX}{bucket_id}/{file_path}")
            out.text("(dry run) 1 file would be removed.")
            return

        out.confirm(f"Remove '{file_path}' from '{bucket_id}'?", yes=yes)

        api.batch_bucket_files(bucket_id, delete=[file_path])
        out.result("File removed", path=file_path, bucket_id=bucket_id)

