
def _get_attr_from_logit_processors(logits_processor, logit_processor_class, attribute_name):
    if logits_processor is not None:
        logit_processor = next((cls for cls in logits_processor if isinstance(cls, logit_processor_class)), None)
        if logit_processor:
            return getattr(logit_processor, attribute_name, None)
    return None

