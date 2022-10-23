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
    gen = Generator("0a0b0cff", "md5", "aes128")
    gen.generate()
    verifier.verify("md5_3des_0a0b0cff.enc")
    verifier.verify("md5_aes128_0a0b0cff.enc")
    cracking.crack("md5_aes128_0a0b0cff.enc")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
