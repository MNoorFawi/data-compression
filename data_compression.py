import pandas as pd
import re
from sys import getsizeof

data = pd.read_csv('german_credit.csv', sep = ',', header = 0)
age = data['Age'] 
getsizeof(list(age))

print("######### Compressing Age and Class variables from GermanCredit data set:\n")

pfor = [i - age.min() for i in age]
b_pfor = max([int(i).bit_length() for i in list(pfor)])
pfor_s = map(str, pfor)
pfor_str = " ".join(pfor_s)

def space_saving(original, compressed):
    return "space saving from original to compressed is {}%".format(
        round((1 - (getsizeof(compressed) / getsizeof(original))) * 100), 2)

print("###### Compressing Age Variable:")

class CompressedAGE:
    def __init__(self, age):
        self._compress(age)
        
    def _compress(self, age):
        self.bit_string = 1 # start with sentinel
        self.minimum = min(list(age))
        self.pfor = [i - self.minimum for i in age]
        self.b_pfor = max([int(i).bit_length() for i in list(self.pfor)])
        self.pfor_s = map(str, self.pfor)
        self.pfor_str = " ".join(self.pfor_s)
        for num in self.pfor_str.split():
            self.bit_string <<= self.b_pfor # shift left with maximum bits
            self.bit_string |= int(('{0:0%sb}' % self.b_pfor).format(int(num)), 2)

    def decompress(self):
        orig_num = ""
        for i in range(0, self.bit_string.bit_length() - 1, self.b_pfor): # - 1 to exclude sentinel
            bits = self.bit_string >> i & int(str(0b1) * self.b_pfor, 2) # get just b_pfor relevant bits
            orig_num += str(bits)[::-1]
            #orig_num += str(bits)
            orig_num += " "
        orig_num = orig_num.rstrip()[::-1]
        return [int(i) + self.minimum for i in orig_num.split()]
    
    def __str__(self): # string representation for pretty printing
        return " ".join(map(str, self.decompress()))


original = list(age)
print("original age variable[0:10]:\n", original[0:10])
print("original age is {} bytes".format(getsizeof(original)))
compressed = CompressedAGE(original) # compress
print("compressed age is {} bytes".format(getsizeof(compressed.bit_string)))
print("compressed age bit_string looks like: {}.....".format(
        str(compressed.bit_string)[0:40]))
#print(compressed) # decompress
print("decompressed age variable[0:10]:\n", compressed.decompress()[0:10])
print("original and decompressed age are the same: {}".format(
    original == compressed.decompress()))
print(space_saving(original, compressed))
compressed_age = compressed.bit_string

print("\n###############################################################\n") 

cls = data["Class"]
getsizeof(list(cls))
#cls2 = " ".join(cls)
#getsizeof(cls2)

print("###### Compressing Class Variable:")

class CompressedCLS:
    def __init__(self, cls):
        self._compress(cls)
        
    def _compress(self, cls):
        self.bit_string = 1 # start with sentinel
        #for cl in cls.split():
        for cl in cls:
            self.bit_string <<= 2 # shift left two bits
            if cl == "Good": # change last two bits to 00
                self.bit_string |= 0b00
            elif cl == "Bad": # change last two bits to 01
                self.bit_string |= 0b01
            else:
                raise ValueError("Invalid class:{}".format(cl))

    def decompress(self):
        cls = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2): # - 1 to exclude sentinel
            bits = self.bit_string >> i & 0b11 # get just 2 relevant bits
            if bits == 0b00: # Good
                cls += "Good"[::-1] # backwards
            elif bits == 0b01: # Bad
                cls += "Bad"[::-1]
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        #return cls[::-1] # [::-1] reverses string by slicing backward
        return re.sub(r"(\w)([A-Z])", r"\1 \2", cls[::-1]).split() # add space before upper letters
    
    def __str__(self): # string representation for pretty printing
        return " ".join(map(str, self.decompress()))

if __name__ == "__main__":
    original = list(cls)
    print("original class variable[0:10]:\n", original[0:10])
    print("original class is {} bytes".format(getsizeof(original)))
    compressed = CompressedCLS(original) # compress
    print("compressed class is {} bytes".format(getsizeof(compressed.bit_string)))
    print("compressed class bit_string looks like: {}.....".format(
        str(compressed.bit_string)[0:40]))
    print("decompressed class variable[0:10]:\n", compressed.decompress()[0:10])
    #print(compressed) # decompress
    print("original and decompressed class are the same: {}".format(
        original == compressed.decompress()))
    print(space_saving(original, compressed))
    compressed_class = compressed.bit_string

# import re
# re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad')
# re.sub(r"(\w)([A-Z])", r"\1 \2", "WordWordWord")

print("\n###### Constructing Compressed Pandas DataFrame ######\n")

original_data = data[["Age", "Class"]]
compressed_data = pd.DataFrame()
compressed_data["compressed_age"] = pd.Series(compressed_age, dtype = object) 
compressed_data["compressed_class"] = pd.Series(compressed_class, dtype = object)
print("original data [0:10]:\n", original_data[0:10])
print("original data dimensions:", original_data.shape)
print("original data is {} bytes\n".format(getsizeof(original_data)))
print("compressed data: (transposed)", compressed_data.T, "\n")
print("compressed data dimensions:", compressed_data.shape)
print("compressed data is {} bytes".format(getsizeof(compressed_data)))
print("")
print(space_saving(original_data, compressed_data))

