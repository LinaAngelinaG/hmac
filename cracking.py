import argparse
import pathlib
from array import array
from multiprocessing import Process, Queue
import time

import generator
from verifier import verify
from generator import Generator


# def crack(args):
#     filename = args.filename
#     if verify(filename):
#         ct_val, gen = parse_file(filename)
#         print("Start cracking ::")
#         ct_count = bytes()
#         incr_pass = 0
#         start = time.time()
#         while ct_val != ct_count.decode():
#             if incr_pass % 32 == 0 & args.verbose:
#                 current = time.time()
#                 print_speed(time.time(), start, gen.password, incr_pass)
#             ct_count = gen.generate()
#             gen.password = incr_p(gen.password, 1)
#             incr_pass += 1
#         if ct_val == ct_count.decode():
#             current = time.time()
#             print("Found password!", incr_pass(gen.password, -1), " | Speed: ",
#                   incr_pass / (current - start), " c/s...")


def crack(filename):
    try:
        file = open("input.txt", "r")
        text = file.readline()
        if verify(filename):
            ct_val, gen = parse_file(filename)
            print("Start cracking ::")
            ct_count = ""
            incr_pass = 0
            start = time.time()
            while not ct_val.__eq__(ct_count):
                if incr_pass % 54240 == 0:
                    print_speed(time.time(), start, gen.password, incr_pass)
                key = gen.hmac()
                ct_count = gen.enc(key, text).hex()
                gen.password = incr_p(gen.password, 1)
                incr_pass += 1
            print(ct_val, ct_count)
            if ct_val.__eq__(ct_count):
                current = time.time()
                print("Found password!", incr_p(gen.password, -1), " | Speed: ",
                      incr_pass / (current - start), " c/s...")
    finally:
        file.close()


def print_speed(current, start, pas1, incr_pass):
    print("Current: ", pas1, " - ", incr_p(pas1, 54240), " | Speed: ",
          incr_pass / (current - start), " c/s...")


def get_enc(s):
    if s == 0:
        return "3des"
    elif s == 1:
        return "aes128"
    elif s == 2:
        return "aes192"
    else:
        return "aes256"


def incr_p(password, inc):
    length = len(password)
    passw_incremented = int.from_bytes(password, 'big', signed=True)
    passw_incremented += inc
    return passw_incremented.to_bytes(length, 'big', signed=True)


def parse_file(filename):
    try:
        file = open(filename, "r")
        text = file.readline()
        enc_f = get_enc(int(text[5:7], base=2))
        hash_f = "md5" if str(int(text[3:5], base=2)).__eq__("0") else "sha1"
        gen = Generator(bytes([0x00, 0x00, 0x00, 0x00]), hash_f, enc_f)
        gen.nonce = int(text[7:7+64*8], base=2).to_bytes(64, 'big', signed=False)
        iv_end = 7+64*8 + gen.get_iv_bytes(enc_f)*8
        gen.iv = int(text[7+64*8:iv_end], base=2).to_bytes(gen.get_iv_bytes(enc_f), 'big', signed=False)
        text = text[iv_end:]
        text = int(text, base=2).to_bytes(len(text)//8, 'big', signed=False).hex()
        print("HMAC: ", hash_f, " ", enc_f)
        print("NONCE: ", gen.nonce)
        print("IV: ", gen.iv)
        print("CT: ", text)
        return text, gen
    finally:
        file.close()


def check_eq(start, end, text, gen, num):
    add = ''
    for i in range(num):
        add = add + '0'
    eq = bytearray(8)
    time_start = time.time()
    count = start
    while start < end:
        print(add + hex(start).replace('0x', ''))
        gen.password = bytearray.fromhex(add + hex(start).replace('0x', ''))
        key = gen.hmac()
        if eq.__eq__(gen.dec(key, text)[:8]):
            print('PASSWORD IS ' + key)
            break
        start = start + 1
    time_end = time.time()
    print("from " + count + " to " + end + " : " + time_end - time_start + " sec" + "\n")


def incr(mas):
    if mas[3] == 255:
        mas[3] = 0
        if mas[2] == 255:
            mas[2] = 0
            if mas[1] == 255:
                mas[1] = 0
                mas[0] = mas[0] + 1
            else:
                mas[1] = mas[1] + 1
        else:
            mas[2] = mas[2] + 1
    else:
        mas[3] = mas[3] + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='run with logs')
    parser.add_argument('filename',
                        type=pathlib.Path,
                        action='store',
                        help='file with info')
    crack(parser.parse_args())
