# Import socket module 
import socket
import random

import importlib

if __name__ == '__main__':

	s = socket.socket()		
	port = 12358
	s.connect(('127.0.0.1', port)) 
	str = (s.recv(1024).decode())
	print(str)

	a = 2
	b = 31
	Gx = 3
	Gy = 8

	if str == 'Send now':
		mod = importlib.import_module('1905012_aes')
		mod2 = importlib.import_module('1905012_df')
		#sending a
		print("Sending a : ")
		print(a)
		num_a = a.__str__()
		s.send(num_a.encode())
		#sending b
		print("Sending b : ")
		print(b)
		num_b = b.__str__()
		s.send(num_b.encode())
		#sending Gx
		print("Sending Gx : ")
		print(Gx)
		num_Gx = Gx.__str__()
		s.send(num_Gx.encode())
		#sending Gy
		print("Sending Gy : ")
		print(Gy)
		num_Gy = Gy.__str__()
		s.send(num_Gy.encode())
		#sending P
		 
		P = mod2.genPrime(128)
		print("Sending P: ")
		print(P)
		num_P = P.__str__()
		s.send(num_P.encode())

		# getting Ka
		lower = (2**128)
		upper = (2**(128+10))
		Ka = random.randint(lower, upper)
		
		ansList = mod2.point_multiplication(a, b, Gx, Gy, Ka, P, 128)
		print("Computed co-ordinates from Alice:")
		print(ansList)

		# sending ansList[0]
		print("Sending GenPoint[0]: ")
		print(ansList[0])
		num_Px = ansList[0].__str__()
		s.send(num_Px.encode())

		ack=s.recv(1024).decode()

		# sending ansList[1] 
		print("Sending GenPoint[1]: ")
		print(ansList[1])
		num_Py = ansList[1].__str__()
		s.send(num_Py.encode())

		ack=s.recv(1024).decode()

		Bx = (s.recv(1024).decode())
		print("Received Bx:")
		print(Bx)

		s.send("ok\n".encode())

		By = (s.recv(1024).decode())
		print("Received By:")
		print(By)

		s.send("ok\n".encode())

		finalList = mod2.point_multiplication(a, b, int(Bx), int(By), Ka, P, 128)
		print("Shared Key Computed from Alice:")
		print(finalList)




        # preparing keyList
		keyList=[]
		num = finalList[0]
		list1_str=''
		while(num>=10):
			dighehe = num %10
			num = num //10
			list1_str += chr(dighehe+48)


		list1_str = list1_str[::-1]
		while (len(list1_str)% 32) != 0:
			list1_str += chr(48)
		 
		for i in range (0,32,2):
			keyList.append(list1_str[i:i+2:1])

		plaintextList = []
		initialVector = []
		for i in range(0,16):
			plaintextList.append(hex(0)[2:])
			initialVector.append(hex(random.randint(0,255))[2:])
    
    	#inputfrom Alice file
		f = open('Alice.txt','r')
		plaintext = f.read()
		print("here is from file\n")
		print(plaintext)
		f.close()
		#plaintext = input()
		

		for element in plaintext:
			plaintextList.append(hex(ord(element))[2:])

		while (len(keyList) % 16) != 0:
			keyList.append(hex(32)[2:])
		while (len(plaintextList) % 16) != 0:
			plaintextList.append(hex(32)[2:])

		keyList2 = []
		for i in range(0,16):
			keyList2.append(keyList[i])

		keyList = keyList2		
		keyList = mod.key_scheduling(keyList)

    	# AES encrypt
		print("The plain text is:\n")
		print(plaintextList)
		
		arrList = mod.AES_encrypt(keyList, plaintextList, initialVector)
		print("\n")
		print("Ciphered Text:")
		print("In HEX: ",end="")
		print(arrList)
		print("In ASCII: ",end="")
		cipher = ' '.join([item for item in arrList])
		print(cipher)
		print('\n')
		print("Sent cipher")
		s.send(cipher.encode())
		s.close()
	else:
		# close the connection 
		s.close()	 
	
