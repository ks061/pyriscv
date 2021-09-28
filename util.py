"""
Name: Kartikeya Sharma
Class: CSCI 320
Professor Marchiori

This file contains the Util
class, which contains utility
functions to be used throughout
the pyriscv project.
"""

""" Utility class """
class Util:
	"""
        Calculates the number of bits needed to
        represent a particular number
        
        :param num: number

        :returns number of bits needed to
                 represent num
        """
	def calc_bit_len(num):
		if num == 1: return 0
		else: return 1 + Util.calc_bit_len(num >> 1)	

