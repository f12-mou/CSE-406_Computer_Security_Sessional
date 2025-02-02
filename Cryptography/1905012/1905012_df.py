import numpy as np
import random
import sympy as smp
from timeit import default_timer as timer
from tabulate import tabulate


def point_addition(x1, y1, x2, y2, mod, k):
	# s = ( (y2-y1) / (x2-x1) ) % mod
	s = (y2 - y1 + mod) % mod
	MI = smp.mod_inverse((x2-x1),mod)
	s = (s * MI) % mod

	# x3 = (s * s - x1 - x2) % mod
	x3 = (s*s)%mod
	x3 = (x3 - x1 + mod)%mod
	x3 = (x3 - x2 + mod)%mod

	# y3 = (s * (x1 - x3) - y1) % mod
	y3 = (x1 - x3 + mod) %mod
	y3 = (y3 * s) %mod
	y3 = (y3 - y1 + mod) % mod
	ans = []
	ans.append(x3)
	ans.append(y3)
	return ans

def point_doubling(a, x1, y1, mod, k):
	s = (x1 * x1) %mod
	s = (s * 3)%mod
	s = (s + a) %mod
	MI = smp.mod_inverse((2*y1), mod)
	s = (s * MI) % mod

	x3 = (s*s)%mod
	x3 = (x3 - x1 + mod)%mod
	x3 = (x3 - x1 + mod)%mod


	y3 = (x1 - x3 + mod) %mod
	y3 = (y3 * s) %mod
	y3 = (y3 - y1 + mod) % mod
	ans = []
	ans.append(x3)
	ans.append(y3)
	return ans


def point_multiplication(a,b, x1, y1, const, modulus, k):
	bv = bin(const)
	found = 0
	result =[x1, y1]
	for i in range(2, len(bv)):
		elem = int(bv[i])
		if ((elem == 1) and (found == 0)):
			found = 1
			continue

		if (found == 1):
			if elem ==1:
				result = point_doubling(a, result[0], result[1], modulus, k)
				result = point_addition(x1, y1, result[0], result[1], modulus,k)
			else:
				result = point_doubling(a, result[0], result[1], modulus, k)
	
	return result
	


def genPrime(k):
	a = (2**k)
	b = (2**(k+10))
	a_randprime_b = smp.randprime(a, b)
	return a_randprime_b

def reportGeneration(a, b, Gx, Gy):
	list_k = [128, 192, 256]
	timeList = []
	for i in range(0,len(list_k)):
		# Getting Prime number P
		k = list_k[i]
		timeList2 =[]
		timeList2.append(k)
		P = genPrime(k)
		print("The prime is: ")
		print(P)
		time_A = 0.0
		time_B = 0.0
		time_R = 0.0
		for j in range(0,5):
			lower = (2**k)
			upper = (2**(k+10))
			Ka = random.randint(lower, upper)
			Kb = random.randint(lower, upper)
			#getting A
			startTime = timer()
			A = point_multiplication(a,b,Gx,Gy,Ka,P,k)
			endTime = timer()
			time_A = time_A + (endTime - startTime)
			#getting B
			startTime = timer()
			B = point_multiplication(a,b,Gx,Gy,Kb,P,k)
			endTime = timer()
			time_B = time_B + (endTime - startTime)
			# getting R
			startTime = timer()
			final1 = point_multiplication(a,b,A[0],A[1],Kb,P,k)
			final2 = point_multiplication(a,b,B[0],B[1],Ka,P,k)
			endTime = timer()
			time_R = time_R + (endTime - startTime)

			if final1 != final2:
				print("Fatal error computing shared key\n")
				break
		
		timeList2.append(time_A/5.0)
		timeList2.append(time_B/5.0)
		timeList2.append(time_R/10.0)
		timeList.append(timeList2)

	print("The time units are(in second)\n")
	print(tabulate(timeList, headers=['K', 'Time_for_A', 'Time_for_B', 'Time_for_R']))


if __name__ == '__main__':
	# 1. Generate the shared parameters G, a, b, and P
	a = 2
	b = 31
	Gx = 3
	Gy = 8	# y^2 = (x^3) + a*x + b

	
	reportGeneration(a, b, Gx, Gy)




	



   


