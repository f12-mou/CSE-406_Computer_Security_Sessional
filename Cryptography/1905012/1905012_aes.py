import numpy as np
from BitVector import *
from timeit import default_timer as timer
import random

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

global_round_constant = ['01', '02', '04', '08', '10', '20', '40', '80', '1B', '36']
global_constant_matrix = ['02','03','01','01',
                          '01','02','03','01',
                          '01','01','02','03',
                          '03','01','01','02']
global_constant_matrix2 = ['0E','0B','0D','09',
                          '09','0E','0B','0D',
                          '0D','09','0E','0B',
                          '0B','0D','09','0E']

AES_modulus = BitVector(bitstring='100011011')

def g_func(w3List, round):
    w3ListNew = w3List[1:] + w3List[:1] # circular byte left shift of w[3]
    addConstantVector = [global_round_constant[round],'00','00','00'] # fetching round constant vector
    start = 0
    w3ListNew2 = []
    for elem in w3ListNew: # There will be a loop of 4 iterations
        here=elem
        b = BitVector(hexstring=here)
        int_val = b.intValue()
        s = Sbox[int_val]           # Byte Substitution (S-Box)
        s = BitVector(intVal=s, size=8)
        here=s.get_bitvector_in_hex()
        bv1 = BitVector( hexstring=here)
        bv2 = BitVector( hexstring = addConstantVector[start])
        start = start + 1
        bv3 = bv1.__xor__(bv2)  # Adding round constant
        w3ListNew2.append(bv3.get_bitvector_in_hex())
    return w3ListNew2


def func2(w0, w1):
    resultList = []
    for i in range(0,4):
        bv1 = BitVector( hexstring=w0[i])
        bv2 = BitVector( hexstring=w1[i])
        bv3 = bv1.__xor__(bv2)
        resultList.append(bv3.get_bitvector_in_hex())
    return resultList


    
    
def func(w0, w1, w2, w3, resultList):
    w4 = func2(w0, resultList) # func2 just returns list (xor of 2 lists) 
    w5 = func2(w1, w4)
    w6 = func2(w2, w5)
    w7 = func2(w3, w6)
    resultList2 = []
    for elem in w4:
        resultList2.append(elem)
    for elem in w5:
        resultList2.append(elem)
    for elem in w6:
        resultList2.append(elem)
    for elem in w7:
        resultList2.append(elem)

    return resultList2
    

def func_list_to_array(list1, row, col):
    arr = np.array(list1)
    newarr = arr.reshape(row, col)
    newarr2 = np.array(list1).reshape(row, col)
    for i in range(0,4):
        for j in range(0,4):
            newarr2[j][i] = newarr[i][j]
    return newarr2

def xor_two_elements(x1, x2):
    bv1 = BitVector( hexstring=x1)
    bv2 = BitVector( hexstring=x2)
    bv3 = bv1.__xor__(bv2)
    return bv3.get_bitvector_in_hex()

def multiply_two_elements(x1, x2):
    bv1 = BitVector(hexstring=x1)
    bv2 = BitVector(hexstring=x2)
    bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
    return bv3.get_bitvector_in_hex()


def xor_two_matrices(arr1, arr2,row):
    arr3 = arr1
    for i in range(0,row):
        for j in range(0,row):
            arr3[i][j] = xor_two_elements(arr1[i][j], arr2[i][j])

    return arr3 
                

def round_0_encryption(keyList, plainTextList):
    arr = func_list_to_array(keyList, 4, 4) # round key 0 matrix
    arr2 = func_list_to_array(plainTextList, 4, 4) # state matrix
    return xor_two_matrices(arr, arr2, 4)

def substitution_encryption(arr, row):
    arr2 = arr
    for i in range(0,row):
        for j in range(0,row):
            elem = arr[i][j]
            b = BitVector(hexstring=elem)
            int_val = b.intValue()
            s = Sbox[int_val]
            s = BitVector(intVal=s, size=8)
            arr2[i][j] = s.get_bitvector_in_hex()
    return arr2

def substitution_decryption(arr, row):
    arr2 = []
    for i in range(0,row):
        for j in range(0,row):
            elem = arr[i][j]
            b = BitVector(hexstring=elem)
            int_val = b.intValue()
            s = InvSbox[int_val]
            s = BitVector(intVal=s, size=8)
            arr2.append(s.get_bitvector_in_hex())
    return np.array(arr2).reshape((row, row))

def shift_row_encryption(arr, row):
    arr2 = arr
    for i in range(0,row):
        here = []
        for j in range(i,row):
            here.append(arr[i][j])
        for j in range(0,i):
            here.append(arr[i][j])
        
        for j in range(0,4):
            arr2[i][j]=here[j]

    return arr2

def shift_row_decryption(arr, row):
    arr2 = []
    for i in range(0,row):
        here = []
        for j in range(row-i,row):
            here.append(arr[i][j])
        for j in range(0,row-i):
            here.append(arr[i][j])
        
        for j in range(0,4):
            arr2.append(here[j])

    return np.array(arr2).reshape((row, row))


def mix_col_encryption(arr):
    arr1 = np.array(global_constant_matrix2).reshape(4,4)
    arr2 = arr
    arr3 = []
    for i in range(4):
    # iterate through columns of Y
        for j in range(4):
            # iterate through rows of Y
            val = '00'
            for k in range(4):
                here =  multiply_two_elements(arr1[i][k], arr2[k][j])
                val = xor_two_elements(val, here)
            arr3.append(val)
 
    return np.array(arr3).reshape(4,4)

def mix_col_decryption(arr):
    arr1 = np.array(global_constant_matrix).reshape(4,4)
    arr2 = arr
    arr3 = []
    for i in range(4):
    # iterate through columns of Y
        for j in range(4):
            # iterate through rows of Y
            val = '00'
            for k in range(4):
                here =  multiply_two_elements(arr1[i][k], arr2[k][j])
                val = xor_two_elements(val, here)
            arr3.append(val)
 
    return np.array(arr3).reshape(4,4)

def encrypt(keyList, plainTextList):
    arr = round_0_encryption(keyList[0:16], plainTextList)
    for x in range(0,10):
        arr=substitution_encryption(arr,4) # substitute each entry (byte) of current state matrix by corresponding entry in AES S-Box
        arr=shift_row_encryption(arr,4) # four rows are shifted cyclically to the left by offsets of 0,1,2, and 3
        # this linear mixing step causes diffusion of the bits over multiple rounds
        if x != 9:
            arr = mix_col_encryption(arr) # Mix Column multiplies fixed matrix against current State Matrix
        arr = xor_two_matrices(arr, func_list_to_array(keyList[16*(x+1):(16*(x+1)+16)],4,4), 4) # 1-based indexing xor , round = x is actually x+1 here
    
    arrList = []
    for i in range(0,4):
        for j in range(0,4):
            arrList.append(arr[j][i]) # col by col
    return arrList
    

def decrypt(keyList, plainTextList):
    arr = round_0_encryption(keyList[(10*16):16+(10*16)], plainTextList)
    for x in range(0,10):
        arr=shift_row_decryption(arr,4)
        arr=substitution_decryption(arr,4)
        arr = xor_two_matrices(arr, func_list_to_array(keyList[16*(10-x-1):(16*(10-x-1)+16)],4,4), 4)
        if x != 9:
            arr = mix_col_decryption(arr)

    arrList = []
    for i in range(0,4):
        for j in range(0,4):
            arrList.append(arr[j][i])
    return arrList


def AES_encrypt(keyList, plaintextList, initialVector): # divides the input into chunks of 16 characters and encrypt them
    arrList = [] # ciphertext holder
 
    for i in range(0,len(plaintextList),16):
        nowInputList = []
        start = 0   # pointing to initial vector position
        for j in range(i,i+16):
            nowInputList.append(hex(int(plaintextList[j],16)^(int(initialVector[start],16)))[2:])
            start = start + 1
        tempList = encrypt(keyList, nowInputList) # nowInputList is the xor ed val of input and initial vector
        for elem in tempList:
            arrList.append(elem)
        initialVector=tempList # for next round, this is the initial vector
    
    return arrList

def AES_decrypt(keyList,arrList): # similar to AES_encrypt
    arrList2 = []   #this will hold initial_vector || input plaintext
    initialVector2 = []
    for i in range(0,16):
        initialVector2.append(hex(0)[2:]) # not going in the calculation of ciphertext part
    for i in range(0,len(arrList),16):
        nowInputList = []
        for j in range(i,i+16):
            nowInputList.append(arrList[j])
            
        tempList = decrypt(keyList, nowInputList)
        start = 0
        for elem in tempList:
            arrList2.append(hex(int(elem,16)^(int(initialVector2[start],16)))[2:])
            start += 1
        initialVector2=nowInputList # next round initial vector, could be done in parallel
    
    return arrList2


def key_scheduling(keyList):
    # Total number of rounds = 10
    for x in range(0,10):
        cuttedList = keyList[(len(keyList)-16):len(keyList):1] # here is the last 16 elements of KeyList
        w0 = cuttedList[0:4:1]      # taking first 4 elements
        w1 = cuttedList[4:8:1]      # taking second 4 elements
        w2 = cuttedList[8:12:1]     # taking third 4 elements
        w3 = cuttedList[12:16:1]    # taking fourth 4 elements
        resultList = g_func(w3,x)   # circular byte left shift, byte substitution, adding constant vector 
        nowGotList = func(w0, w1, w2, w3, resultList) # got the 16 keys for current round x
        for elem in nowGotList:
            keyList.append(elem)

    return keyList # final keyList containing all keys





if __name__ == '__main__':
    input_key = input()
    f = open('in.txt','r')
    plaintext = f.read()
    f.close()
    keyList = []
    plaintextList = []
    initialVector = []
    for i in range(0,16):
        plaintextList.append(hex(0)[2:]) # for propagating initialization vector, we are prepending 16 zeros
        initialVector.append(hex(random.randint(0,255))[2:]) # random vector of length 16
    
    for element in input_key:
        keyList.append(hex(ord(element))[2:]) # converting the key from ASCII from HEX

    for element in plaintext:
        plaintextList.append(hex(ord(element))[2:]) # converting the plaintext from ASCII to HEX

    while (len(keyList) % 16) != 0:
        keyList.append(hex(32)[2:]) # making sure that length is multiple of 16
    while (len(plaintextList) % 16) != 0:
        plaintextList.append(hex(32)[2:]) # making sure that length is multiple of 16
        

    # here we are taking the first 16 characters as the key (for simplicity)
    keyList2 = []
    for i in range(0,16):
        keyList2.append(keyList[i])

    keyList = keyList2


    # key Printing
    print("Key:")
    str_key = ""
    for elem in keyList:
        str_key += chr(int(elem, 16))
    
    print("In ASCII: ", end="")
    print(str_key)
    print("In HEX: ", end="")
    print(keyList)
    print("\n")
    # plainText printing

    print("Plain Text:")
    str_plain = ""
    for i in range(16,len(plaintextList)):
        str_plain += chr(int(plaintextList[i], 16))
    
    print("In ASCII: ", end="")
    print(str_plain)
    print("In HEX: ", end="")
    print(plaintextList)
    key_time = 0
    encryption_time = 0
    decryption_time = 0
    

    # key Scheduling
    startTime = timer()
    keyList = key_scheduling(keyList)
    endTime = timer()
    key_time = (endTime - startTime) * 1000
    

    # AES encrypt
    startTime = timer()
    arrList = AES_encrypt(keyList, plaintextList, initialVector)
    endTime = timer()
    encryption_time = (endTime - startTime) * 1000

    print("\n")
    print("Ciphered Text:")
    print("In HEX: ",end="")
    print(arrList)
    print("In ASCII: ",end="")
    cipher = ""
    for elem in arrList:
        cipher += chr(int(elem, 16))
    print(cipher)

    # AES decrypt
    startTime = timer()
    arrList2 = AES_decrypt(keyList, arrList)
    endTime = timer()
    decryption_time = (endTime - startTime) * 1000

    print("\n")
    print("Deciphered Text:")
    print("In HEX: ",end="")
    print(arrList2)
    print("In ASCII: ",end="")
    decipher = ""
    for i in range(16, len(arrList2)):
        decipher += chr (int(arrList2[i],16))
    print(decipher)
    
    print("Execution Time Details:")
    print("Key Schedule Time: ", end="")
    print(key_time, end="")
    print(" ms")
    print("Encryption Time: ", end="")
    print(encryption_time, end="")
    print(" ms")
    print("Decryption Time: ", end="")
    print(decryption_time, end="")
    print(" ms")
    
    

