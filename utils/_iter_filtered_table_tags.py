from typing import List, Optional

def _iter_filtered_table_tags(
    tags: Iterable[str],
    include_tables: Optional[List[str]] = None,
    exclude_tables: Optional[List[str]] = None,
) -> Iterator[str]:
    for tag in tags:
        if exclude_tables and tag in exclude_tables:
            continue
        if include_tables and tag not in include_tables:
            continue
        yield tag

