
def _in_memory_output_stream_context() -> Iterator[TextIO]:
    yield StringIO(newline=None)

