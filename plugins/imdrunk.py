from util import hook

@hook.regex("i'm drunk")
def crymebot(match):
    return "me too lol"