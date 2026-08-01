
def build_pages_from_reducto(result: Dict[str, Any]) -> List["OCRPage"]:
    from litellm.llms.base_llm.ocr.transformation import OCRPage

    chunks = result.get("chunks", []) or []
    blocks_by_page: Dict[int, List[Dict[str, Any]]] = defaultdict(list)

    for chunk in chunks:
        for block in chunk.get("blocks", []) or []:
            page_no = (block.get("bbox") or {}).get("page")
            if page_no is None:
                continue
            try:
                normalized_page = int(page_no)
            except (TypeError, ValueError):
                continue
            blocks_by_page[normalized_page].append(block)

    if not blocks_by_page:
        fallback_markdown = "\n\n".join(
            chunk.get("content", "") for chunk in chunks if chunk.get("content")
        )
        if fallback_markdown == "":
            return []
        return [OCRPage(index=0, markdown=fallback_markdown)]

    pages: List["OCRPage"] = []
    for page_no, blocks in sorted(blocks_by_page.items()):
        markdown = "\n\n".join(
            block.get("content", "") for block in blocks if block.get("content")
        )
        page_index = max(page_no - 1, 0)
        page = OCRPage(
            index=page_index,
            markdown=markdown,
        )
        # OCRPage accepts extra keys at runtime; assign blocks after construction
        # so static typing does not reject provider-specific metadata.
        setattr(page, "blocks", blocks)
        pages.append(page)
    return pages

