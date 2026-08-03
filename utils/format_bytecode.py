from typing import Any

def format_bytecode(table):
    # given a nested tuple, convert it to nested list
    def listify(content):
        if not isinstance(content, tuple):
            return content
        return [listify(i) for i in content]

    formatted_table = {}
    for entry in table:
        identifier = entry[0]
        content = entry[1]
        content = listify(content)
        formatted_table[identifier] = content
    return formatted_table


def format_bytecode(
    prefix: str, name: str, filename: str, line_no: int, code: Any
) -> str:
    return f"{prefix} {name} {filename} line {line_no} \n{dis.Bytecode(code).dis()}\n"

