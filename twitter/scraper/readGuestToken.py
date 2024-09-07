file_path = "twitter/guest_token.txt"


def readGuestTokentxt():
    with open(file_path, "r") as file:
        content = file.read()
    return content


def writeGuestTokentxt(value):
    with open(file_path, "w") as file:
        file.write(f"{value}")
    return True
