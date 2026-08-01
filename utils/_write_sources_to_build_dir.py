
def _write_sources_to_build_dir(sources, build_dir):
    build_dir = build_dir or tempfile.mkdtemp()
    if not os.path.isdir(build_dir):
        raise OSError("Non-existent directory: ", build_dir)

    source_files = []
    for name, src in sources:
        dest = os.path.join(build_dir, name)
        differs = True
        sha256_in_mem = sha256_of_string(src.encode('utf-8')).hexdigest()
        if os.path.exists(dest):
            if os.path.exists(dest + '.sha256'):
                sha256_on_disk = Path(dest + '.sha256').read_text()
            else:
                sha256_on_disk = sha256_of_file(dest).hexdigest()

            differs = sha256_on_disk != sha256_in_mem
        if differs:
            with open(dest, 'wt') as fh:
                fh.write(src)
            with open(dest + '.sha256', 'wt') as fh:
                fh.write(sha256_in_mem)
        source_files.append(dest)
    return source_files, build_dir

