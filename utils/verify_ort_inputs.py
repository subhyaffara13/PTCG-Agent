
def verify_ort_inputs(model: InferenceSession, ort_inputs: dict):
    # Check that all model inputs will be provided
    model_inputs = {model_input.name for model_input in model.get_inputs()}
    user_inputs = set(ort_inputs.keys())
    missing_inputs = model_inputs - user_inputs
    if len(missing_inputs):
        print(f"The following model inputs are missing: {missing_inputs}")
        raise Exception("There are missing inputs to the model. Please add them and try again.")

    # Remove unnecessary inputs from model inputs
    unnecessary_inputs = user_inputs - model_inputs
    if len(unnecessary_inputs):
        for unnecessary_input in unnecessary_inputs:
            del ort_inputs[unnecessary_input]

    return ort_inputs

