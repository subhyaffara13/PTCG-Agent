
def parse_battles_dataset(filter_ties=False):
  """Parse the data set from the raw CSV."""
  dataset = []
  model_names = {}
  with gfile.Open(DATASET_FILE, "r") as f:
    lines = f.readlines()
  for line in lines:
    if line.startswith("#"):
      continue
    # ,question_id,model_a,model_b,winner,judge,conversation_a,conversation_b,turn,anony,language,tstamp,openai_moderation,toxic_chat_tag
    parts = line.split(",")
    model_a, model_b, winner = (
        parts[2].strip(),
        parts[3].strip(),
        parts[4].strip(),
    )
    if filter_ties and winner.startswith("tie"):
      continue
    else:
      model_names[model_a] = True
      model_names[model_b] = True
      if winner == "model_a":
        dataset.append((model_a, model_b, -1))
      elif winner == "model_b":
        dataset.append((model_a, model_b, 1))
      else:
        assert winner.startswith("tie")
        dataset.append((model_a, model_b, 0))
  return list(model_names.keys()), dataset

