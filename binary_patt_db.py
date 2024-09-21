#@mcdouglasx
import secp256k1 as ice
import random
import regex as re
from bitarray import bitarray
import sys

target_public_key = "0339d69444e47df9bd7bb7df2d234185293635a41f0b0c7a4c37da8db5a74e9f21"

num_keys = 120000000
subtract = 1
low_m = num_keys // 1000000
lm = num_keys // low_m

db_name = "patt_db.txt"

patternx = re.compile(r'((10)+1|(01)+0)')

def process_res(res, lm, prev_bits=None):
    binary = bitarray()
    if prev_bits:
        binary.extend(prev_bits)
    
    for t in range(lm):
        segment = res[t*65:t*65+65]
        bit = '0' if int(segment.hex()[2:], 16) % 2 == 0 else '1'
        binary.append(bit == '1')
    
    return binary

def count_patterns(binary_bits, total_bits):
    matches = patternx.finditer(binary_bits.to01())
    last_end = 0
    for match in matches:
        pattern = match.group()
        if len(pattern) >= 15:
            bits_between = match.start() - last_end
            total_bits += bits_between + len(pattern)
            last_end = match.end()
            with open(db_name, 'a') as f:
                f.write(f"Bi: {bits_between}, Pp: {pattern}, Tb: {total_bits}\n")
    
    remaining_bits = len(binary_bits) - last_end
    next_prev_bits = binary_bits[-remaining_bits:]
    
    return total_bits, next_prev_bits

print("Making DataBase")

target = ice.pub2upub(target_public_key)
subtract_pub = ice.scalar_multiplication(subtract)
prev_bits = None
total_bits = 0  

for i in range(low_m):
    sys.stdout.write(f"\rprogress: {i + 1}/{low_m}")
    sys.stdout.flush()
    lm_i = lm * i
    lm_upub = ice.scalar_multiplication(lm_i)
    A1 = ice.point_subtraction(target, lm_upub)
    res = ice.point_loop_subtraction(lm, A1, subtract_pub)
    binary_bits = process_res(res, lm, prev_bits)
    total_bits, prev_bits = count_patterns(binary_bits, total_bits)

print("\nDone!")
