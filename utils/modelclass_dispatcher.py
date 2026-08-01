
def modelclass_dispatcher(model_name, custom_model_class):
    if custom_model_class is not None:
        if custom_model_class in MODEL_CLASSES:
            return custom_model_class
        else:
            raise Exception("Valid model class: " + " ".join(MODEL_CLASSES))

    if model_name in PRETRAINED_GPT2_MODELS:
        return "GPT2ModelNoPastState"

    import re  # noqa: PLC0415

    if re.search("-squad$", model_name) is not None:
        return "AutoModelForQuestionAnswering"
    elif re.search("-mprc$", model_name) is not None:
        return "AutoModelForSequenceClassification"
    elif re.search("gpt2", model_name) is not None:
        return "AutoModelWithLMHead"

    return "AutoModel"

