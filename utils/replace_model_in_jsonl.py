import json

def replace_model_in_jsonl(file_content: FileTypes, new_model_name: str) -> FileTypes:
    try:
        ## if pathlike, return the original file content
        if isinstance(file_content, PathLike):
            return file_content

        # Iterate the source line-by-line WITHOUT reading it all into memory. A
        # spooled upload handle (managed batches stream from it) is read straight
        # off its backing; bytes/str are wrapped so they iterate line-by-line.
        source = file_content[1] if isinstance(file_content, tuple) else file_content
        if hasattr(source, "read"):
            if hasattr(source, "seek"):
                try:
                    source.seek(0)  # type: ignore[attr-defined]
                except (OSError, ValueError):
                    pass
            line_iter: object = source
        elif isinstance(source, (bytes, bytearray)):
            line_iter = io.BytesIO(bytes(source))
        elif isinstance(source, str):
            line_iter = io.StringIO(source)
        else:
            return file_content

        # Rewrite one row at a time, writing straight into the output buffer
        # instead of holding every parsed row in a list. Peak memory stays at
        # ~one row plus the output rather than several full copies of the file,
        # which the managed-files path depends on (it re-runs this rewrite once
        # per target model). Lines are accumulated so JSON objects that span
        # multiple physical lines still parse. Streaming the handle also means
        # the model rewrite is actually applied to tuple-wrapped upload handles;
        # otherwise a restricted body.model would survive and bypass the batch
        # model allowlist (which validates the upload target alias).
        output = InMemoryFile(
            b"", name="modified_file.jsonl", content_type="application/jsonl"
        )
        wrote_any = False
        buffer = ""
        for raw_line in line_iter:  # type: ignore[attr-defined]
            buffer += (
                raw_line.decode("utf-8")
                if isinstance(raw_line, (bytes, bytearray))
                else raw_line
            )
            stripped = buffer.strip()
            if not stripped:
                buffer = ""
                continue
            try:
                json_object = json.loads(stripped)
            except json.JSONDecodeError:
                continue  # object not complete yet; keep accumulating
            if isinstance(json_object, dict) and isinstance(
                json_object.get("body"), dict
            ):
                json_object["body"]["model"] = new_model_name
            output.write(
                (("\n" if wrote_any else "") + json.dumps(json_object)).encode("utf-8")
            )
            wrote_any = True
            buffer = ""

        if buffer.strip():
            # A row never parsed (truncated/malformed, or it swallowed the rows
            # that followed it). Returning the partial `output` would silently
            # drop those rows; return the unchanged original so the provider
            # rejects the batch loudly instead of accepting a truncated one.
            verbose_logger.error(
                f"error parsing trailing batch content: {buffer[:100]}..."
            )
            if hasattr(source, "seek"):
                try:
                    source.seek(0)  # type: ignore[attr-defined]
                except (OSError, ValueError):
                    pass
            return file_content

        # If no valid JSON objects were found, return the original content
        if not wrote_any:
            return file_content

        output.seek(0)
        return output  # type: ignore

    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        # return the original file content if there is an error replacing the model name
        return file_content

