
def composite_rules(rule1, rule2):
  if not rule1 and not rule2:
    return ()
  if rule1 and not rule2:
    return rule1
  if rule2 and not rule1:
    return rule2
  rules = {alias: value for alias, value in rule1}
  for alias, value in rule2:
    if alias in rules and rules[alias] != value:
      raise ValueError(
          f'Inconsistent logical axis annotations for {alias}: '
          f'{rules[alias]} vs {value}'
      )
    rules[alias] = value
  return tuple(rules.items())

