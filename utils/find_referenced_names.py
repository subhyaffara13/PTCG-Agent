
def find_referenced_names(file: MypyFile) -> set[str]:
    finder = ReferenceFinder()
    file.accept(finder)
    return finder.refs

