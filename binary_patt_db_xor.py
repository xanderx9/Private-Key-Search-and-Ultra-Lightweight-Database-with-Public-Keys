#@mcdouglasx
import secp256k1 as ice
import random
import regex as re
from bitarray import bitarray
import sys
import hashlib
import pickle

target_public_key = "0339d69444e47df9bd7bb7df2d234185293635a41f0b0c7a4c37da8db5a74e9f21"

num_keys = 120000000
subtract = 1
low_m = num_keys // 1000000
lm = num_keys // low_m

patternx = re.compile(r'((10)+1|(01)+0)')


class XORFilter:
    def __init__(self, size):
        self.size = size
        self.filter = bitarray(size)
        self.filter.setall(0)
        self.data = {}
        self.num_elements = 0

    def _hash(self, element, seed):
        return int(hashlib.blake2b((str(seed) + element).encode(), digest_size=8).hexdigest(), 16) % self.size

    def add(self, element, number):
        positions = [self._hash(element, i) for i in range(2)]
        for pos in positions:
            self.filter[pos] ^= 1
        self.data[element] = number
        self.num_elements += 1 
        self._adjust_size()  

    def contains(self, element):
        positions = [self._hash(element, i) for i in range(2)]
        if all(self.filter[pos] for pos in positions):
            return self.data.get(element, None)
        return None

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            loaded_filter = pickle.load(f)
            self.filter = loaded_filter.filter
            self.data = loaded_filter.data
            self.num_elements = len(self.data)  

    def _adjust_size(self):
        load_factor = self.num_elements / self.size
        if load_factor > 0.5:
            new_size = self.size * 2
            new_filter = bitarray(new_size)
            new_filter.setall(0)
            for element, number in self.data.items():
                positions = [self._hash(element, i) for i in range(2)]
                for pos in positions:
                    new_filter[pos] ^= 1
            self.filter = new_filter
            self.size = new_size



initial_size = 1000
xor_filter = XORFilter(initial_size)
try:
    xor_filter.load("patt_db.pkl")
except FileNotFoundError:
    pass

def process_res(res, lm, prev_bits=None):
    binary = bitarray()
    if prev_bits:
        binary.extend(prev_bits)
    
    for t in range(lm):
        segment = res[t*65:t*65+65]
        bit = '0' if int(segment.hex()[2:], 16) % 2 == 0 else '1'
        binary.append(bit == '1')
    
    return binary

def count_patterns(binary_bits, total_bits, xor_filter):
    matches = patternx.finditer(binary_bits.to01())
    last_end = 0
    for match in matches:
        pattern = match.group()
        if len(pattern) >= 15:
            bits_between = match.start() - last_end
            total_bits += bits_between + len(pattern)
            last_end = match.end()
            xor_filter.add(f"Bi: {bits_between}, Pp: {pattern}", total_bits)
    
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
    total_bits, prev_bits = count_patterns(binary_bits, total_bits, xor_filter)
    
    xor_filter.save("patt_db.pkl")

print("\nDone!")
