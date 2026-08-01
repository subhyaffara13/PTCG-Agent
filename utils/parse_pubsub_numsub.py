
def parse_pubsub_numsub(command, res, **options):
    numsub_d = OrderedDict()
    for numsub_tups in res.values():
        for channel, numsubbed in numsub_tups:
            try:
                numsub_d[channel] += numsubbed
            except KeyError:
                numsub_d[channel] = numsubbed

    ret_numsub = [(channel, numsub) for channel, numsub in numsub_d.items()]
    return ret_numsub


def parse_pubsub_numsub(response, **options):
    return list(zip(response[0::2], response[1::2]))

