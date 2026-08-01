
def _iter_openai_jsonl_entries(
    openai_file_content: FileTypes,
) -> Iterator[Dict[str, Any]]:
    for line in _iter_openai_jsonl_lines(openai_file_content):
        yield json.loads(line)

