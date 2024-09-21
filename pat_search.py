import secp256k1 as ice
import random
import regex as re
from bitarray import bitarray
import time

print("Searching Binary Patterns")

#Pk: 10056435896
#0339d69444e47df9bd7bb7df2d234185293635a41f0b0c7a4c37da8db5a74e9f21

Target_pub ="0339d69444e47df9bd7bb7df2d234185293635a41f0b0c7a4c37da8db5a74e9f21"
#range 
start = 10000000000                                                                                
end =  12000000000                                      


with open('patt_db.txt', 'r') as Db:
    target = Db.readlines()

patternx = re.compile(r'((10)+1|(01)+0)')

def process_res(res, low_m):
    binary = bitarray()
    
    for t in range(low_m):
        segment = res[t*65:t*65+65]
        bit = '0' if int(segment.hex()[2:], 16) % 2 == 0 else '1'
        binary.append(bit == '1')
    
    return binary

def count_patterns(binary_bits, Rand, start_time):
    matches = patternx.finditer(binary_bits.to01())
    last_end = 0
    last_match_info = None
    
    for match in matches:
        pattern = match.group()
        if len(pattern) >= 15:
            bits_between = match.start() - last_end
            total_bits = match.start()  
            
            last_end = match.end()
            
            X = f"Bi: {bits_between}, Pp: {pattern}"
            for t in target:
                if X in t:
                    Tb_in_t = int(t.split(", Tb: ")[1].split(",")[0])
                    pk = (Rand - total_bits + Tb_in_t)-len(pattern)
                    pk_f = ice.scalar_multiplication(pk).hex()
                    cpub = ice.to_cpub(pk_f)
                    if cpub in Target_pub:
                        last_match_info = f"Rand: {Rand} Bi: {bits_between}, Pp: {pattern}, Tb: {total_bits}, T: {t.strip()}, pk: {pk}"
                  
    
    if last_match_info:
        pk_f = ice.scalar_multiplication(pk).hex()
        cpub = ice.to_cpub(pk_f) 
        elapsed_time = time.time() - start_time
        print("pk:", pk)
        print("cpub:", cpub)
        print("Elapsed time:", elapsed_time, "seconds")
        
        with open('found.txt', 'a') as f:
            f.write(f"pk: {pk}\n")
            f.write(f"cpub: {cpub}\n")
            f.write(f"Elapsed time: {elapsed_time} seconds\n")       
        exit()

low_m = 100000
sustract = 1
sustract_pub = ice.scalar_multiplication(sustract)        
start_time = time.time()

while True:
    
    Rand = random.randint(start, end)
    pk = ice.scalar_multiplication(Rand)
    res = ice.point_loop_subtraction(low_m, pk, sustract_pub)
    binary_bits = process_res(res, low_m)
    count_patterns(binary_bits, Rand, start_time)
    
