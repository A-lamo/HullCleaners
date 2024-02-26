import numpy as np
from fractions import Fraction

def FLCM(arr):  # Fractional Least Common Multiple
	num = arr[0]
	den = arr[1]
	
	fractions_lst = [Fraction(num,den), Fraction(1, 1)]
	
	lcm = np.lcm.reduce([fr.denominator for fr in fractions_lst])
	vals = [int(fr.numerator * lcm / fr.denominator) for fr in fractions_lst]
	vals.append(lcm)
	print("VALS : ",vals)
	
	return vals
