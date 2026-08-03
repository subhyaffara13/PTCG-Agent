import os

def _build_one_inside_env(
    req: InstallRequirement,
    output_dir: str,
    editable: bool,
) -> str | None:
    with TemporaryDirectory(dir=output_dir) as wheel_directory:
        assert req.name
        assert req.metadata_directory
        assert req.pep517_backend
        if editable:
            wheel_path = build_wheel_editable(
                name=req.name,
                backend=req.pep517_backend,
                metadata_directory=req.metadata_directory,
                wheel_directory=wheel_directory,
            )
        else:
            wheel_path = build_wheel_pep517(
                name=req.name,
                backend=req.pep517_backend,
                metadata_directory=req.metadata_directory,
                wheel_directory=wheel_directory,
            )

        if wheel_path is not None:
            wheel_name = os.path.basename(wheel_path)
            dest_path = os.path.join(output_dir, wheel_name)
            try:
                wheel_hash, length = hash_file(wheel_path)
                # We can do a replace here because wheel_path is guaranteed to
                # be in the same filesystem as output_dir. This will perform an
                # atomic rename, which is necessary to avoid concurrency issues
                # when populating the cache.
                os.replace(wheel_path, dest_path)
                logger.info(
                    "Created wheel for %s: filename=%s size=%d sha256=%s",
                    req.name,
                    wheel_name,
                    length,
                    wheel_hash.hexdigest(),
                )
                logger.info("Stored in directory: %s", output_dir)
                return dest_path
            except Exception as e:
                logger.warning(
                    "Building wheel for %s failed: %s",
                    req.name,
                    e,
                )
        return None

