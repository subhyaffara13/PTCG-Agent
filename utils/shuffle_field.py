import random

def shuffle_field(agents, field_name):
    values = [agent[field_name] for agent in agents]
    random.shuffle(values)
    for agent, value in zip(agents, values):
        agent[field_name] = value

