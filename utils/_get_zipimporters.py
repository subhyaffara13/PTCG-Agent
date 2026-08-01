
def _get_zipimporters() -> Iterator[tuple[str, zipimport.zipimporter]]:
    for filepath, importer in sys.path_importer_cache.items():
        if importer is not None and isinstance(importer, zipimport.zipimporter):
            yield filepath, importer

