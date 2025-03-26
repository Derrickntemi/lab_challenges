# This is the program we believe was used to encode the intercepted message.
# some of the retrieved program was damaged (show as &&&&)
# Can you use this to figure out how it was encoded and decode it? 
# Good Luck
import random
import string
from base64 import b64encode, b64decode

secret = '&&&&&&&&&&&&&&'  # We don't know the original message or length

secret_encoding = ['step1', 'step2', 'step3']


# substitution
def step1(s):
    _step1 = str.maketrans("zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA",
                           "mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON")
    return str.translate(s, _step1)


def step2(s):
    return b64encode(s.encode()).decode()


# Diffusion
def step3(plaintext, shift=4):
    loweralpha = string.ascii_lowercase
    shifted_string = loweralpha[shift:] + loweralpha[:shift]
    converted = str.maketrans(loweralpha, shifted_string)
    return plaintext.translate(converted)


def make_secret(plain, count):
    a = '2{}'.format(b64encode(plain.encode()).decode())
    for count in range(count):
        r = random.choice(secret_encoding)
        si = secret_encoding.index(r) + 1
        _a = globals()[r](a)
        a = '{}{}'.format(si, _a)
    return a


def decrypt(cipher_text):
    try:
        if cipher_text[:1].isdigit():
            step = int(cipher_text[:1])
            step_index = int(step) - 1
            operation = secret_encoding[step_index]
            function = globals()[operation]
            print(f'Performing the {operation}')
            if operation == 'step2':
                return decrypt(b64decode(cipher_text[1:]).decode())
            elif operation == 'step3':
                return decrypt(function(cipher_text[1:], shift=-4))
            else:
                return decrypt(function(cipher_text[1:]))
        else:
            return cipher_text
    except UnicodeDecodeError as e:
        print(f"An error has occurred: {e}")
        return ""


if __name__ == '__main__':
    with open('intercepted_message.txt', 'r') as f:
        cipher_text = f.read()
        plain_text = decrypt(cipher_text)
        print(f'The plain text is: {plain_text}')
