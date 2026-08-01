
def represent_list(self, data):
    """Compact lists"""
    flow_style = not any(isinstance(i, dict) for i in data)
    return self.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=flow_style)

