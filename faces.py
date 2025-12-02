IDLE = [1,
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "/\\   /\\",
    "   w   "
],
[
    "__   __",
    "   w   "
]] #idle

LISTENING = [1,
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "()   ()",
    "   w   "
],
[
    "__   __",
    "   w   "
]] #listening

THINKING = [1.5,
[
    "(?) (*)",
    "   w   "
],
[
    "(*) (?)",
    "   w   "
]]

SPEAKING = [4,
[
    "/\\   /\\",
    "   O   "
],
[
    "/\\   /\\",
    "   -   "
]]

def get(face):
    if face == "IDLE":
        return IDLE
    elif face == "LISTENING":
        return LISTENING
    elif face == "THINKING":
        return THINKING
    elif face == "SPEAKING":
        return SPEAKING
    else:
        Print("ERROR: Invalid face")