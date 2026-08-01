
def convert_requires(requires: str, metadata: Message) -> None:
    extra: str | None = None
    requirements: dict[str | None, list[str]] = defaultdict(list)
    for line in requires.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("[") and line.endswith("]"):
            extra = line[1:-1]
            continue

        requirements[extra].append(line)

    for key, value in generate_requirements(requirements):
        metadata.add_header(key, value)

