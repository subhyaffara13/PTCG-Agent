
def _add_GSUB_feature_variations(
    font, axes, internal_axis_supports, rules, featureTags
):
    def normalize(name, value):
        return models.normalizeLocation({name: value}, internal_axis_supports)[name]

    log.info("Generating GSUB FeatureVariations")

    axis_tags = {name: axis.tag for name, axis in axes.items()}

    conditional_subs = []
    for rule in rules:
        region = []
        for conditions in rule.conditionSets:
            space = {}
            for condition in conditions:
                axis_name = condition["name"]
                if condition["minimum"] is not None:
                    minimum = normalize(axis_name, condition["minimum"])
                else:
                    minimum = -1.0
                if condition["maximum"] is not None:
                    maximum = normalize(axis_name, condition["maximum"])
                else:
                    maximum = 1.0
                tag = axis_tags[axis_name]
                space[tag] = (minimum, maximum)
            region.append(space)

        subs = {k: v for k, v in rule.subs}

        conditional_subs.append((region, subs))

    addFeatureVariations(font, conditional_subs, featureTags)

