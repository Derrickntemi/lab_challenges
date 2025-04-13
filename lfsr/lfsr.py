def xor_hex_strings(hex1: str, hex2: str):
    # Convert hex to bytes
    bytes1 = bytes.fromhex(hex1)
    bytes2 = bytes.fromhex(hex2)

    # Determine the longer and shorter byte sequences
    if len(bytes1) > len(bytes2):
        long_bytes, short_bytes = bytes1, bytes2
    else:
        long_bytes, short_bytes = bytes2, bytes1

    # pad with zeros
    padded_short_bytes = short_bytes.ljust(len(long_bytes) - len(short_bytes), b'0')

    # XOR the two byte sequences
    res = bytes((a ^ b) for a, b in zip(long_bytes, padded_short_bytes))
    return res.hex()


def get_first_8_bytes_of_key_stream():
    """ The first 8 bytes of all PNG images are the same. Hence, we can xor the known bytes with the cipher text to retrieve the first 8 bytes of the keystream. """
    known_png_bytes = '89504e470d0a1a0a'
    with open('flag.enc', 'rb') as f:
        cipher_text_hex = bytes.hex(f.read())
        key_stream_8_bytes = xor_hex_strings(known_png_bytes, cipher_text_hex[:16])
        return key_stream_8_bytes


def lfsr(state, taps):
    feedback = feedback_fn(state, taps)
    next = state.pop()
    state.insert(0, feedback)
    return state, next


def feedback_fn(state, taps):
    feedback = 0
    for tap in taps:
        feedback ^= state[tap - 1]
    return feedback


# Combine function
def combine(state1_combine_bits, state2_combine_bits):
    result = bytearray()
    i = 0
    while i < 64:
        register_1_bin = ''.join(str(j) for j in state1_combine_bits[i:i + 8])
        register_2_bin = ''.join(str(j) for j in state2_combine_bits[i:i + 8])
        register_1_state = int(register_1_bin, 2)
        register_2_state = int(register_2_bin, 2)
        combine_result = (register_1_state + register_2_state) % 255
        result.append(combine_result)
        i += 8
    return result.hex()


# get 8 bytes of key stream
known_key_stream_bits = get_first_8_bytes_of_key_stream()

if __name__ == '__main__':
    # Try all possible keys
    for s1 in range(1, 2 ** 12):
        for s2 in range(1, 2 ** 19):
            state1 = [int(_) for _ in format(s1, '012b')]
            state2 = [int(_) for _ in format(s2, '019b')]
            state1_combine_bits = []
            state2_combine_bits = []
            for _ in range(64):
                state1, out1 = lfsr(state1, taps=[2, 7])
                state2, out2 = lfsr(state2, taps=[5, 11])
                state1_combine_bits.append(out1)
                state2_combine_bits.append(out2)

            combine_result = combine(state1_combine_bits, state2_combine_bits)
            print(f"Comparing: {combine_result} and {known_key_stream_bits}")
            if combine_result == known_key_stream_bits:
                print(f"Key found: {state1_combine_bits}, {state2_combine_bits}")
                break
