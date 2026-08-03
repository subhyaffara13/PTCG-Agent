import json

def get_tensor_quant_overrides(file):
    # TODO: Enhance the function to handle more real cases of json file
    if not file:
        return {}
    with open(file) as f:
        quant_override_dict = json.load(f)
    for tensor in quant_override_dict:
        for enc_dict in quant_override_dict[tensor]:
            enc_dict["scale"] = np.array(enc_dict["scale"], dtype=np.float32)
            enc_dict["zero_point"] = np.array(enc_dict["zero_point"])
    return quant_override_dict

