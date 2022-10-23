import re


def verify(filename):
    text = open(filename, "r").readline()
    min_length = int(text[4])*8 + 8 + 1 + 64
    max_length = min_length + 4095
    print(min_length, len(text[5:]), text[4])

    match = re.fullmatch('ENC[0-1]{1}[0-3]{1}[a-f0-9]{' + str(min_length) +"," + str(max_length) + "}"  , text)
    print("True" if match else "False")
    return match
