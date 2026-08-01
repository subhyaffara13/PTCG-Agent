
def find_defined_names(file: MypyFile) -> set[str]:
    finder = DefinitionFinder()
    file.accept(finder)
    return finder.names

