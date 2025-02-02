# first of all import the socket library 
import socket
import random	
import importlib	 

if __name__ == '__main__':
	s = socket.socket()		 
	print ("Socket successfully created")
	port = 12358			

	s.bind(('', port))		 
	print ("socket binded to %s" %(port)) 
	s.listen(5)	 
	print ("socket is listening")		  
	while True: 
		mod = importlib.import_module('1905012_aes')
		mod2 = importlib.import_module('1905012_df')

		c, addr = s.accept()	 
		print ('Got connection from', addr )
 
		c.send('Send now'.encode()) 

		a = (c.recv(1024).decode())
		print("Received a:")
		print(a)
		b = (c.recv(1024).decode())
		print("Received b:")
		print(b)
		Gx = (c.recv(1024).decode())
		print("Received Gx:")
		print(Gx)
		Gy = (c.recv(1024).decode())
		print("Received Gy:")
		print(Gy)
		P = (c.recv(1024).decode())
		print("Received P:")
		print(P)

		# getting Kb
		lower = (2**128)
		upper = (2**(128+10))
		Kb = random.randint(lower, upper)

		ansList = mod2.point_multiplication(int(a), int(b), int(Gx), int(Gy), Kb, int(P), 128)
		print("Computed co-ordinates from Bob:")
		print(ansList)

		Ax = (c.recv(1024).decode())
		print("Received Ax:")
		print(Ax)
		c.send("ok\n".encode())
		Ay = (c.recv(1024).decode())
		print("Received Ay:")
		print(Ay)

		c.send("ok\n".encode())
		# sending ansList[0]
		print("Sending GenPoint[0]: ")
		print(ansList[0])
		num_Px = ansList[0].__str__()
		c.send(num_Px.encode())

		ack=c.recv(1024).decode()

		# sending ansList[1] 
		print("Sending GenPoint[1]: ")
		print(ansList[1])
		num_Py = ansList[1].__str__()
		c.send(num_Py.encode())

		ack=c.recv(1024).decode()

		finalList = mod2.point_multiplication(int(a), int(b), int(Ax), int(Ay), Kb, int(P), 128)
		print("Shared Key Computed from bob:")
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

		while (len(keyList) % 16) != 0:
			keyList.append(hex(32)[2:])

		keyList2 = []
		for i in range(0,16):
			keyList2.append(keyList[i])
		
		keyList = keyList2		
		keyList = mod.key_scheduling(keyList)
    	# AES decrypt
		str = c.recv(1024).decode()
		arrList = str.split()
		print("I got from Alice\n")
		print(arrList)

		arrList2 = mod.AES_decrypt(keyList, arrList)
		print("\n")
		print("Deciphered Text:")
		print("In HEX: ",end="")
		print(arrList2)
		print("In ASCII: ",end="")
		decipher = ""
		for i in range(16, len(arrList2)):
			decipher += chr (int(arrList2[i],16))
		print(decipher)

		# Close the connection with the client 
		c.close()

		# Breaking once connection closed
		break
