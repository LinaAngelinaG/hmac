import argparse
import pathlib
import re
import generator


def verify(filename):
    text = open(filename, "r").readline()
    file_parameters = str(filename).split('_')
    return check_file(file_parameters, text[:7], len(text))


def check_file(params, text, text_len):
    match = re.fullmatch('ENC0[0-1]{1}[0-1]{1}[0-1]{1}', text)
    min_len = ((int(text[4]) * 8) * 2 + 8 + 1 + 64 + 3)*8
    gen = generator.Generator
    result = match
    if int(gen.enc_func_id.get(params[1])) == int(text[5:7], base=2):
        if int(gen.hash_func_id.get(params[0])) == int(text[3:5], base=2):
            if min_len <= text_len:
                result = match
            else:
                result = False
        else:
            result = False
    else:
        result = False
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        type=pathlib.Path,
                        action='store',
                        help='file with encrypted text')
    res = verify(parser.parse_args().filename)
    print("True" if res else "False")
