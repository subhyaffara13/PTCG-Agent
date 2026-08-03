import os

def update_path(path, shard_index=0, num_shards=1):
  """Regenerates all playthroughs in the path."""
  if os.path.isfile(path):
    file_list = [path]
  else:
    file_list = sorted(os.listdir(path))
  for filename in file_list[shard_index::num_shards]:
    try:
      original, kwargs = _read_playthrough(os.path.join(path, filename))
      try:
        pyspiel.load_game(kwargs["game_string"])
      except pyspiel.SpielError as e:
        if "Unknown game" in str(e):
          print(f"\x1b[0J[Skipped] Skipping game {filename} as ",
                f"{kwargs['game_string']} is not available.")
          continue
        else:
          raise
      new = playthrough(**kwargs)
      if original == new:
        print(f"\x1b[0J        {filename}", end="\r")
      else:
        with open(os.path.join(path, filename), "w") as f:
          f.write(new)
        print(f"\x1b[0JUpdated {filename}")
    except Exception as e:  # pylint: disable=broad-except
      print(f"\x1b[0J{filename} failed: {e}")
      raise

