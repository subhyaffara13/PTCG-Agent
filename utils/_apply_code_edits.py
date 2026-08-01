
def _apply_code_edits(edits):
    for edit in edits.get("files_to_edit", []):
        fp = pathlib.Path(edit["filepath"])
        if fp.exists():
            content = fp.read_text(encoding="utf-8")
            if edit["original_code"] in content:
                content = content.replace(edit["original_code"], edit["new_code"])
                fp.write_text(content, encoding="utf-8")
                logger.info(f"LLM successfully patched {fp.name}")
            else:
                logger.warning(f"LLM provided mismatched original_code for {fp.name}")

