
def new_debate_scenario_config(
    config: ml_collections.config_dict.ConfigDict,
    game_id: int,
) -> ml_collections.config_dict.ConfigDict:
  """Creates a new debate scenario config with a new topic.

  Arguments:
    config: the original debate scenario config dict (this should contain
      examples for generating new scenarios)
    game_id: int, will index into set of 20 debate topics found in
      https://www.englishclub.com/speaking/agreeing-disagreeing-topics.php
  Returns:
    new_config: debate config with redefined debate topic
  """
  # https://www.englishclub.com/speaking/agreeing-disagreeing-topics.php
  topics = ["Breakfast is the most important meal of the day.",
            "Swimming in the ocean is better than swimming in a public pool.",
            "Alcohol should be illegal.",
            "Children should provide room and board for their aging parents.",
            "Studying grammar is more important than practising conversation " +
            "skills.",
            "Television is the leading cause of violence in todays society.",
            "Dogs make better companions than cats.",
            "Smoking should be permitted in public places.",
            "Females are better students than males.",
            "A parent shouldn't pierce a babys ears.",
            "Women should be allowed to go topless in public.",
            "Lawyers should make a higher salary than nurses.",
            "Everyone should plan their own funeral.",
            "Reading English is more difficult than writing English.",
            "Summer is the best season of the year.",
            "Children under 13 should not be allowed to babysit.",
            "High school students should wear uniforms.",
            "21 should be the legal driving age around the world.",
            "Rock and Roll is the best kind of music.",
            "The government should pay for post secondary education."]

  topic = topics[game_id]
  config.game.given_private_info["topic"] = [topic, topic]

  return config

