"""
Name: Kartikeya Sharma
Class: CSCI 320
Professor Marchiori

This file contains the function make_mux 
that creates and returns a multiplexer and 
contains tests for verifying the functionality
of that multiplexer.
"""
# filename: mux.py
"""
    Creates a multiplexer with the array of functions in
    args as the inputs to the multiplexer.

    :param args: array of functions to serve as inputs
		 into the multiplexer
"""
def make_mux(*args):
   return lambda i: (args)[i]() if (i>=0 and i<len(args)) else None
                                          # i is the selection bit
	    				  # of the multiplexer

if __name__=="__main__": 
   # test 1: analogous to the test
   # given in lab 03, part 1
   print("Test 1")

   i = None

   mux = make_mux(lambda: 1,
		  lambda: 2,
		  lambda: 3,
		  lambda: 4,
		  lambda: 5)

   for i in range(5):
       print(f"mux({i}) == {mux(i)}")
   
   print("\n")   

   # test 2: testing with functions
   # with different parameters
   # (testing higher level of complexity)
   print("Test 2")

   i2 = None
   def test_func1(d={"Angry": "Birds", "Professor": "King"}, k="Angry"):
       return d[k]
   def test_func3(j=64):
       return j >> 1
   def test_func5():
       return "I like apple pie"

   mux = make_mux(test_func1,
		  lambda: 0x11,
		  test_func3,
		  lambda: "Prof. Marchiori",
		  test_func5)

   i2 = 0
   print(f"Expected: mux({i2}) == Birds")
   print(f"Actual: mux({i2}) == {mux(i2)}")

   i2 = 1
   print(f"Expected: mux({i2}) == 17")
   print(f"Actual: mux({i2}) == {mux(i2)}")

   i2 = 2
   print(f"Expected: mux({i2}) == 32")
   print(f"Actual: mux({i2}) == {mux(i2)}")

   i2 = 3
   print(f"Expected: mux({i2}) == Prof. Marchiori")
   print(f"Actual: mux({i2}) == {mux(i2)}")

   i2 = 4
   print(f"Expected: mux({i2}) == I like apple pie")
   print(f"Actual: mux({i2}) == {mux(i2)}")
