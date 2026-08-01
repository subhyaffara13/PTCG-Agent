
def get_stack_above_dynamo() -> StackSummary:
    return filter_stack(extract_stack())

