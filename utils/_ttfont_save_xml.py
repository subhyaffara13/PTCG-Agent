from typing import Any, List, Optional

def _ttfont_save_xml(
    ttf: Any,
    filepath: Text,
    include_tables: Optional[List[Text]],
    exclude_tables: Optional[List[Text]],
) -> bool:
    """Writes TTX specification formatted XML to disk on filepath."""
    ttf.saveXML(filepath, tables=include_tables, skipTables=exclude_tables)
    return True

