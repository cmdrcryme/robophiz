from util import hook

@hook.regex("hup")
def crymebot(match):
    return "hup"