import os

def write_legacy_hdf(output_dir, format):
    import tables

    pth = f"{platform_name()}_pytables-{tables.__version__}_{format}.h5"

    df = create_dataframe_all_types()
    if format == "fixed":
        # df = df.drop(columns=["categorical", "categorical_object", "categorical_int"])
        df = df.drop(columns=["categorical_int"])
    complevel = 9 if format == "table" else None
    df.to_hdf(
        os.path.join(output_dir, pth),
        key="df_alltypes",
        format=format,
        complevel=complevel,
    )

    print(f"created hdf file: {pth}")

