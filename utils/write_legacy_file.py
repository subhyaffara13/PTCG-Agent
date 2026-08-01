
def write_legacy_file():
    # force our cwd to be the first searched
    sys.path.insert(0, "")

    if not 3 <= len(sys.argv) <= 4:
        sys.exit(
            "Specify output directory and storage type: generate_legacy_"
            "storage_files.py <output_dir> <storage_type> "
        )

    output_dir = str(sys.argv[1])
    storage_type = str(sys.argv[2])

    print(
        "This script generates a storage file for the current arch, system, "
        "and python version"
    )
    print(f"  pandas version: {pandas.__version__}")
    print(f"  output dir    : {output_dir}")
    print(f"  storage format: {storage_type}")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if storage_type == "pickle":
        write_legacy_pickles(output_dir=output_dir)
    elif storage_type == "hdf":
        write_legacy_hdf(output_dir=output_dir, format="fixed")
        write_legacy_hdf(output_dir=output_dir, format="table")
    else:
        sys.exit("storage_type must be one of {'pickle', 'hdf'}")

