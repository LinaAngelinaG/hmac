from array import array
from multiprocessing import Process, Queue
import time

import generator
from verifier import verify
from generator import Generator


def crack(filename):
    if verify(filename):
        num_points = array('i', (0 for i in range(9)))
        for i in range(9):
            num_points[i] = i * (2 ^ 30)
        try:
            file = open(filename, "r")
            text = file.readline()
            enc_f = get_enc(text[4])
            gen = Generator(bytearray(4).hex(), "md5" if text[3].__eq__("0") else "sha1", enc_f)
            gen.nonce = bytearray.fromhex(text[5:69])
            iv_end = 69 + gen.get_iv_bytes(enc_f)
            gen.iv = bytearray.fromhex(text[69:iv_end])
            text = text[iv_end:]
            procs = []
            for i in range(8):
                proc = Process(target=check_eq, args=(num_points[i], num_points[i+1], text, gen, 8-i))
                procs.append(proc)
                proc.start()
            for proc in procs:
                proc.join()
        finally:
            file.close()


def get_enc(s):
    if s.__eq__("0"):
        return "3des"
    elif s.__eq__("1"):
        return "aes128"
    elif s.__eq__("2"):
        return "aes192"
    else:
        return "aes256"


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
