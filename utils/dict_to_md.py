
def dict_to_md(results):
    md_string = '''
| Filename | Name | Type | Start:End Line | Complexity | Classification |
| -------- | ---- | ---- | -------------- | ---------- | -------------- |
'''
    type_letter_map = {'class': 'C',
                       'method': 'M',
                       'function': 'F'}
    for filename, blocks in results.items():
        for block in blocks:
            raw_classname = block.get("classname")
            raw_name = block.get("name")
            name = "{}.{}".format(
                raw_classname,
                raw_name) if raw_classname else block["name"]
            type = type_letter_map[block["type"]]
            md_string += "| {} | {} | {} | {}:{} | {} | {} |\n".format(
                filename,
                name,
                type,
                block["lineno"],
                block["endline"],
                block["complexity"],
                block["rank"])
    return md_string

