import json

def load_jsonl_data(filename):
  with gfile.Open(filename) as f:
    return [json.loads(ljson) for ljson in f.readlines()]

