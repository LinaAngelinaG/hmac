# This is a sample Python script.
import cracking
import verifier
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from generator import Generator

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gen = Generator("000004ff", "md5", "aes128")
    print(gen.iv.decode(), '   and   ', gen.nonce.decode())
    # print(bytearray.fromhex("000004ff"))
    gen.generate()
    # print("True" if verifier.verify("md5_3des_0a0b0cff.enc")
    #       else "False")
    print("True" if verifier.verify("md5_aes128_000004ff.enc")
          else "False")

    cracking.crack("md5_aes128_000004ff.enc")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
