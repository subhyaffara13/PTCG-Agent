
def escape_tex(text, commandprefix):
    return text.replace('\\', '\x00'). \
                replace('{', '\x01'). \
                replace('}', '\x02'). \
                replace('\x00', rf'\{commandprefix}Zbs{{}}'). \
                replace('\x01', rf'\{commandprefix}Zob{{}}'). \
                replace('\x02', rf'\{commandprefix}Zcb{{}}'). \
                replace('^', rf'\{commandprefix}Zca{{}}'). \
                replace('_', rf'\{commandprefix}Zus{{}}'). \
                replace('&', rf'\{commandprefix}Zam{{}}'). \
                replace('<', rf'\{commandprefix}Zlt{{}}'). \
                replace('>', rf'\{commandprefix}Zgt{{}}'). \
                replace('#', rf'\{commandprefix}Zsh{{}}'). \
                replace('%', rf'\{commandprefix}Zpc{{}}'). \
                replace('$', rf'\{commandprefix}Zdl{{}}'). \
                replace('-', rf'\{commandprefix}Zhy{{}}'). \
                replace("'", rf'\{commandprefix}Zsq{{}}'). \
                replace('"', rf'\{commandprefix}Zdq{{}}'). \
                replace('~', rf'\{commandprefix}Zti{{}}')

