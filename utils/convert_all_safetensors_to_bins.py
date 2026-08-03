import json
import os

def convert_all_safetensors_to_bins(folder: str):
    """Convert all safetensors files into torch bin files, to mimic saving with torch (since we still support loading
    bin files, but not saving them anymore)"""
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".safetensors"):
            new_path = path.replace(".safetensors", ".bin").replace("model", "pytorch_model")
            state_dict = load_file(path)
            os.remove(path)
            torch.save(state_dict, new_path)
        # Adapt the index as well
        elif file == SAFE_WEIGHTS_INDEX_NAME:
            new_path = os.path.join(folder, WEIGHTS_INDEX_NAME)
            with open(path) as f:
                index = json.loads(f.read())
            os.remove(path)
            if "weight_map" in index.keys():
                weight_map = index["weight_map"]
                new_weight_map = {}
                for k, v in weight_map.items():
                    new_weight_map[k] = v.replace(".safetensors", ".bin").replace("model", "pytorch_model")
            index["weight_map"] = new_weight_map
            with open(new_path, "w") as f:
                f.write(json.dumps(index, indent=4))

