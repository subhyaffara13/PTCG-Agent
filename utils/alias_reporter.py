
def alias_reporter(source_reporter: str, target_reporter: str) -> None:
    reporter_classes[target_reporter] = reporter_classes[source_reporter]

