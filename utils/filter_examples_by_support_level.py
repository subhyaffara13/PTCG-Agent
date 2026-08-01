
def filter_examples_by_support_level(support_level: SupportLevel):
    return {
        key: val
        for key, val in all_examples().items()
        if val.support_level == support_level
    }

