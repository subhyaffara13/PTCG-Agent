
def direct_url_for_editable(source_dir: str) -> DirectUrl:
    return DirectUrl(
        url=path_to_url(source_dir),
        dir_info=DirInfo(editable=True),
    )

