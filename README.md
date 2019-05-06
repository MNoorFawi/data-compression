# data-compression

Suppose you want to read large data into memory, store very big data into desk when you don’t have much space or even transfer data for example model predictions through api. 
In such situations and in many others you will need data compression.
Here I tried to use python and compression techniques to compress data of numeric and/or categorical variables for better data storage and transfer.

``` python
python data_compression.py

######### Compressing Age and Class variables from GermanCredit data set:

###### Compressing Age Variable:
original age variable[0:10]:
 [67, 22, 49, 45, 53, 35, 53, 35, 61, 28]
original age is 9112 bytes
compressed age is 828 bytes
compressed age bit_string looks like: 2649857614701777378485660885771988844155.....
decompressed age variable[0:10]:
 [67, 22, 49, 45, 53, 35, 53, 35, 61, 28]
original and decompressed age are the same: True
space saving from original to compressed is 99%

###############################################################

###### Compressing Class Variable:
original class variable[0:10]:
 ['Good', 'Bad', 'Good', 'Good', 'Bad', 'Good', 'Good', 'Good', 'Good', 'Bad']
original class is 9112 bytes
compressed class is 292 bytes
compressed class bit_string looks like: 1221011526771983419993684773743626727824.....
decompressed class variable[0:10]:
 ['Good', 'Bad', 'Good', 'Good', 'Bad', 'Good', 'Good', 'Good', 'Good', 'Bad']
original and decompressed class are the same: True
space saving from original to compressed is 99%

###### Constructing Compressed Pandas DataFrame ######

original data [0:10]:
    Age Class
0   67  Good
1   22   Bad
2   49  Good
3   45  Good
4   53   Bad
5   35  Good
6   53  Good
7   35  Good
8   61  Good
9   28   Bad
original data dimensions: (1000, 2)
original data is 68804 bytes

compressed data: (transposed)           
                                                                  0
compressed_age    2649857614701777378485660885771988844155400824...
compressed_class  1221011526771983419993684773743626727824950443... 

compressed data dimensions: (1, 2)
compressed data is 1240 bytes

space saving from original to compressed is 98%
```
