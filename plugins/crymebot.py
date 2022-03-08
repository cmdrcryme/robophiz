from util import hook

@hook.regex("crymebot")
def crymebot(match):
    return "CRYMEBOT LIVES!"