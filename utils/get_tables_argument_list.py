from typing import List, Optional

def get_tables_argument_list(table_list: Optional[List[Text]]) -> Optional[List[Text]]:
    """Converts a list of OpenType table string into a Python list or
    return None if the table_list was not defined (i.e., it was not included
    in an option on the command line). Tables that are composed of three
    characters must be right padded with a space."""
    if table_list is None:
        return None
    else:
        return [table.ljust(4) for table in table_list]

