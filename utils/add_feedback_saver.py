
def add_feedback_saver(
    fn: FeedbackFunction,
):
    cache = get_algorithm_selector_cache()
    cache.add_feedback_saver(fn)

