def destroy(who=None):
    if who == "You":
        return """You stopped the dialog 🙄
Type /next to find a new partner
"""
    elif who == "Your":
        return """Your partner has stopped the dialog 😞
Type /next to find a new partner
"""


def invalid_destroy():
    return """You have no partner 🤔
Type /next to find a new partner"""
