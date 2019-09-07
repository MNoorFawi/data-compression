import pandas as pd
import re
from sys import getsizeof
import numpy as np
from collections import Counter
from  more_itertools import unique_everseen
from itertools import accumulate
import random

def space_saving(original, compressed):
    return "space saving from original to compressed is {}%".format(
        round((1 - (getsizeof(compressed) / getsizeof(original))) * 100), 2)

class compressed_numeric:
    def __init__(self, numeric_data):
        self._compress(numeric_data)
        
    def _compress(self, numeric_data):
        self.num_sorted = sorted(numeric_data, key = Counter(numeric_data).get, reverse = True)
        self.set_num = list(unique_everseen(self.num_sorted))
        self.bits = list(range(0, len(self.set_num)))
        self.dictionary = dict(zip(self.set_num, self.bits))
        self.original = map(str, numeric_data)
        self.original = " ".join(self.original)

        self.bit_integer = 1 
        for num in numeric_data:
            self.bit_integer <<=  self.dictionary[num].bit_length() 
            self.bit_integer |= self.dictionary[num]

    def decompress(self):
        numeric_data = [int(num) for num in self.original.split()]
        x = [int(v).bit_length() for n in numeric_data for k, v in self.dictionary.items() if k == n]
        bs = x[::-1]
        x.append(0)
        x = x[::-1]
        x = list(accumulate(x[:-1]))
        
        orig_num = ""
        for i, b in zip(x, bs):
            bv = str(0b1) * b
            if bv == '':
                bv = 0b0
            else:
                bv = int(bv, 2)
            bits = self.bit_integer >> i & bv
            orig_num += str(next((k for k, v in self.dictionary.items() if v == bits), None))
            orig_num += " "
        orig_num = orig_num.rstrip()

        return [int(i) for i in orig_num.split()[::-1]]
    
    def sampling(self, start, end):
        numeric_data = [int(num) for num in self.original.split()]
        x = [int(v).bit_length() for n in numeric_data[:end] for k, v in self.dictionary.items() if k == n]
        starting_bit = sum(x[:start]) 
        end_bit = starting_bit + sum(x[start:])
        
        sample_bits = int('1' + 
                          bin(self.bit_integer)[3:][starting_bit:end_bit], 2)
        x = x[start:end]
        bs = x[::-1]
        x.append(0)
        x = x[::-1]
        x = list(accumulate(x[:-1]))
        
        orig_num = ""
        for i, b in zip(x, bs):
            bv = str(0b1) * b
            if bv == '':
                bv = 0b0
            else:
                bv = int(bv, 2)
            bits = sample_bits >> i & bv
            orig_num += str(next((k for k, v in self.dictionary.items() if v == bits), None))
            orig_num += " "
        orig_num = orig_num.rstrip()

        return [int(i) for i in orig_num.split()[::-1]]
    
    def info(self):
        numeric_data = [int(num) for num in self.original.split()]
        length = len(numeric_data)
        minimum = min(numeric_data)
        maximum = max(numeric_data)
        average = np.mean(numeric_data)
        std = np.std(numeric_data)
        common_number = self.set_num[0]
        number_of_occ = numeric_data.count(common_number)
        original_size = getsizeof(numeric_data)
        compressed_size = getsizeof(self.bit_integer)
        number_of_bits = self.bit_integer.bit_length()
        
        print('Length of Original Data:', length)
        print('Summary Statistics:\n', '\tMin:' , minimum, '\n\tMax:', maximum,
              '\n\tMean:', average, '\n\tStandard Deviation:', std)
        print('Most Common Number:', common_number, 
              '\n\tNumber of Occurence:', number_of_occ)
        print('Original Size of Data:', original_size)
        print('Compressed Size:', compressed_size)
        print('Number of Bits to Encode Data:', number_of_bits)
    
    def __str__(self):
        start = random.randint(0, len(numeric_data) - 1)
        end = start + 10
        print('a sample from original data:\n', 'from', start, 'to', end)
        return " ".join(map(str, self.sampling(start, end)))
        
class compressed_string:
    def __init__(self, string):
        self._compress(string)
        
    def _compress(self, string):
        self.keys = set(string)
        self.n = len(self.keys)
        self.nrows = len(string)
        self.frequency = dict((x, string.count(x)) for x in self.keys)
        self.bins = list(range(self.n)) 
        self.bit_value = max([i.bit_length() for i in self.bins]) 
        self.bins = [('{0:0%sb}' % self.bit_value).format(int(num)) for num in self.bins]
        self.dictionary = dict(zip(self.keys, self.bins))
        
        self.bit_integer = 1 
        for cl in string:
            self.bit_integer <<= self.bit_value
            self.bit_integer |= int(self.dictionary[cl], 2)

    def decompress(self):
        orig_str = ""
        for i in range(0, self.bit_integer.bit_length() - 1, self.bit_value):
            bits = self.bit_integer >> i & int(str(0b1) * self.bit_value, 2)
            orig_str += next((k for k, v in self.dictionary.items() if int(v, 2) == bits), None)[::-1]

        return re.sub(r"([A-Z])", r" \1", orig_str[::-1]).split()
    
    def sampling(self, start, end):
        starting_bit = start * self.bit_value
        end_bit = end * self.bit_value
        sample_comp = int('1' + bin(self.bit_integer)[3:][starting_bit:end_bit], 2)

        sample_str = ""
        for i in range(0, sample_comp.bit_length() - 1, self.bit_value):
            bits = sample_comp >> i & int(str(0b1) * self.bit_value, 2)
            sample_str += next((k for k, v in self.dictionary.items() if int(v, 2) == bits), None)[::-1]
            
        return re.sub(r"([A-Z])", r" \1", sample_str[::-1]).split()
    
    def info(self):
        compressed_size = getsizeof(self.bit_integer)
        number_of_bits = self.bit_integer.bit_length()
        
        print('Length of Original Data:', self.nrows)
        print('Number of Unique Values in Data:', self.n)
        print('Frequency of Each Unique Value:\n', self.frequency)
        print('Bit Symbol assigned to each value:\n', self.dictionary)
        print('Compressed Size:', compressed_size)
        print('Number of Bits to Encode Data:', number_of_bits)
    
    def __str__(self):
        start = random.randint(0, self.nrows - 1)
        end = start + 10
        print('a sample from original data:\n', 'from', start, 'to', end)
        return " ".join(map(str, self.sampling(start, end)))

    
