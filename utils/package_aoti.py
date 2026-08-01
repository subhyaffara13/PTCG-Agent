
def package_aoti(
    archive_file: FileLike,
    aoti_files: AOTI_FILES,
) -> FileLike:
    """
    Saves the AOTInductor generated files to the PT2Archive format.

    Args:
        archive_file: The file name to save the package to.
        aoti_files: This can either be a singular path to a directory containing
        the AOTInductor files, or a dictionary mapping the model name to the
        path to its AOTInductor generated files.
    """

    return package_pt2(
        archive_file,
        aoti_files=aoti_files,
    )

