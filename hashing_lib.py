import time, math
import random
from matplotlib.pyplot import *
import pandas as pd
import json

num_of_passwords = 100000000
tolerance = 0.01
num_of_bits = int(- num_of_passwords * math.log(tolerance) / math.log(2)**2)
num_of_functons = int(num_of_bits / num_of_passwords * math.log(2))

def my_hash(s, seed = 1):
    ''' This is simplified version of murmur hash 
    '''
    prime = 4194301
    
    val = seed
    length = len(s)
    for i in range(len(s)):
        block_index = i % 4
        #  Each symbol (8 bit) of string 's' moved to one of 4 blocks of 8 bits. Then XOR applies for corresponding block.
        #  "The XOR function is 50% 0 and 50% 1, therefore it is good for combining uniform probability distributions."
        #  - https://stackoverflow.com/questions/5889238/why-is-xor-the-default-way-to-combine-hashes
        val ^= (ord(s[i])) << (block_index * 8)
        
        #  This is so called rotate operation: bits are moved 15 position left and first 15 bits added by logical OR to the end.
        val  = (val << 15) | (val >> 17)  
        
        #  Multiplying by prime number
        val *= prime
        
        #  This is logical mod. Getting getting last 32 bits of number 
        val &= 0xffffffff
        
    #  The last bits shuffling. Constants are taken from: https://github.com/aappleby/smhasher/wiki/MurmurHash3
    val ^= (val >> 16)
    val *= 2246822507 # 0x85ebca6b
    val ^= (val >> 13)
    val *= 3266489909 # 0xc2b2ae35
    val ^= (val >> 16)
    
    return val

def test_my_hash(N = 10000):
    ''' Test of uniformity on random strings of 20 characters
    '''
    start = time.time()
    res = []
    letters = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    num_of_chars = 20
    num_of_iter = N
    for k in range(1,num_of_iter):
        #  Generating random string of size 'num_of_chars'
        s = ''.join(random.choice(letters) for _ in range(num_of_chars)) + '\n'
        
        #  Hasing 'num_of_functons' times and adding to the resulting list
        for j in range(1, num_of_functons+1):
            h = my_hash(s, j) % (N//100)
            res.append(h)

    print(f'Time of {num_of_iter} iterations', time.time() - start)
    
    #  Histogram of distribution
    a = hist(res, bins=100)
    
    
def test_my_hash_2():
    ''' Test on a vocabulary from the third homework
    '''
    with open("../HW_3/vocabulary.json", 'r') as file:
        data = json.load(file)
        res = []
    
    for k in data:
        h = my_hash(k)
        res.append(h % 100)
        
    hist(res,bins=100)
    
def switch_bloom(bloom_bits, s):
    '''  Switching bits of bloom filter 
    '''
    #  Hashing string 's' with a different seed = k. 
    for k in range(1, num_of_functons + 1):
        h = my_hash(s, k) % num_of_bits
        bloom_bits[h] = 1
        
def add_passwords(file_name = 'sorted.txt'):
    ''' The function creates bloom filter 
    '''
    #  Create list of 100000 zeroes
    bloom_bits = [0] * num_of_bits
    with open(file_name, 'r') as file:
        while True:
            line = file.readline().strip()  # line is a password
            if not line:
                break
            
            #  Switch bits for the password 
            switch_bloom(bloom_bits, line)
    
    return bloom_bits
            

def check_passwords(bloom_bits, file_name = 'passwords2.txt'):
    total_number = 0
    duplicates = 0
    with open(file_name, 'r') as file:
        while True:
            line = file.readline().strip()
            if not line:
                break
            
            found = 0  # How many bits of =1 will be found 
            for k in range(1, num_of_functons + 1):
                h = my_hash(line, k) % num_of_bits
                if not bloom_bits[h]:
                    #  if a bit is zero a password is definitly not in bloom filter.
                    break
                else:
                    found += 1 

            #  If number of found bits is equal to number of hash functions then password is presumably duplicate
            if found == num_of_functons:
                duplicates += 1
         
    return duplicates


def real_duplicates():
    '''  The function performs binary search on sorted passwords from passwords1.txt, for each passwords from passwords2.txt
    '''
    line_size = 21
    num_lines = num_of_passwords
    real_duplicates = 0
    cur_index = 0

    #  The file 'sorted.txt' was made by unix command 'sort'. There are sorted lines from passwords1.txt 
    with open('sorted.txt','r') as file:
        with open('passwords2.txt', 'r') as file_to_check:
            while True:
                cur_index += 1
                find = file_to_check.readline()

                start = 0
                end = num_lines - 1
                while start <= end:
                    line_pos = (start + end) // 2
                    #  Since we know that each row has 21 character, we can compute position of the beggining of needed row
                    seek_pos = line_size * line_pos 

                    #  Go to ccomputed position in file and read the line
                    file.seek(seek_pos)
                    line = file.readline()

                    if line > find:
                        end = line_pos - 1
                    elif line < find:
                        start = line_pos + 1
                    else:
                        #  Match of password. Increase counter, break the loop.
                        real_duplicates += 1
                        break


    print("The exact number of duplicates: ", real_duplicates)   

       