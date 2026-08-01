
def _gather_unique_untuned_gemm_from_files(filename_pattern: str) -> set[str]:
    r"""Process multiple untuned results file and return a set with duplicates removed."""
    unique_gemm_entries = set()  # set will avoid duplicates

    for file_path in glob.glob(filename_pattern):
        with open(file_path) as file:
            for line in file:
                if line.startswith(("Gemm", "ScaledGemm")):
                    unique_gemm_entries.add(line)

    return unique_gemm_entries

