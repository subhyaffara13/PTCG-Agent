
def represent_dict(self, data):
    """Compact dicts"""
    return self.represent_mapping("tag:yaml.org,2002:map", data, flow_style=False)

