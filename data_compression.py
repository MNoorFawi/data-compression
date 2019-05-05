import pandas as pd
data = pd.read_csv('german_credit.csv', sep = ',', header = 0)

age = data['Age'] 
from sys import getsizeof
getsizeof(list(age))

pfor = [i - age.min() for i in age]
b_pfor = max([int(i).bit_length() for i in list(pfor)])
pfor_s = map(str, pfor)
pfor_str = " ".join(pfor_s)

class CompressedAGE:
    def __init__(self, age: str) -> None:
        self._compress(age)
        
    def _compress(self, age: str) -> None:
        self.bit_string: int = 1 # start with sentinel
        self.minimum = min(list(age))
        self.pfor = [i - self.minimum for i in age]
        self.b_pfor = max([int(i).bit_length() for i in list(self.pfor)])
        self.pfor_s = map(str, self.pfor)
        self.pfor_str = " ".join(self.pfor_s)
        for num in self.pfor_str.split():
            self.bit_string <<= self.b_pfor # shift left with maximum bits
            self.bit_string |= int(('{0:0%sb}' % self.b_pfor).format(int(num)), 2)

    def decompress(self) -> str:
        orig_num = ""
        for i in range(0, self.bit_string.bit_length() - 1, self.b_pfor): # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & int(str(0b1) * self.b_pfor, 2) # get just b_pfor relevant bits
            orig_num += str(bits)[::-1]
            #orig_num += str(bits)
            orig_num += " "
        orig_num = orig_num.rstrip()[::-1]
        return [int(i) + self.minimum for i in orig_num.split()]
    
    def __str__(self) -> str: # string representation for pretty printing
        return " ".join(map(str, self.decompress()))



from sys import getsizeof
original = list(age)
print("original is {} bytes".format(getsizeof(original)))
compressed: CompressedAGE = CompressedAGE(original) # compress
print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
print(compressed) # decompress
print("original and decompressed are the same: {}".format(original == compressed.decompress()))

################################################ 

cls = data["Class"]
getsizeof(list(cls))
#cls2 = " ".join(cls)
#getsizeof(cls2)

class CompressedCLS:
    def __init__(self, cls: str) -> None:
        self._compress(cls)
        
    def _compress(self, cls: str) -> None:
        self.bit_string: int = 1 # start with sentinel
        #for cl in cls.split():
        for cl in cls:
            self.bit_string <<= 2 # shift left two bits
            if cl == "Good": # change last two bits to 00
                self.bit_string |= 0b00
            elif cl == "Bad": # change last two bits to 01
                self.bit_string |= 0b01
            else:
                raise ValueError("Invalid class:{}".format(cl))

    def decompress(self) -> str:
        cls: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2): # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11 # get just 2 relevant bits
            if bits == 0b00: # A
                cls += "Good"[::-1] # backwards
            elif bits == 0b01: # C
                cls += "Bad"[::-1]
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        #return cls[::-1] # [::-1] reverses string by slicing backward
        return re.sub(r"(\w)([A-Z])", r"\1 \2", cls[::-1]).split() # add space before upper letters
    
    def __str__(self) -> str: # string representation for pretty printing
        return " ".join(map(str, self.decompress()))

if __name__ == "__main__":
    #from sys import getsizeof
    original = list(cls)
    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedCLS = CompressedCLS(original) # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
    print(compressed) # decompress
    print("original and decompressed are the same: {}".format(original == compressed.decompress()))

# import re
# re.findall('[A-Z][^A-Z]*', 'TheLongAndWindingRoad')
# re.sub(r"(\w)([A-Z])", r"\1 \2", "WordWordWord")









