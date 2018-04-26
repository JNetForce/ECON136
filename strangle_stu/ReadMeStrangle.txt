This is file ReadMeStrangle.txt, distributed with strangle_stu.py on April 15, 
2018 in zip file strangle_stu.zip.

This zip file includes a utility file, finutil_stu, which includes the core 
utilities used in many of the options pricing models, and strangle_stu.py, 
which requires input from the user about stock prices, call and put bids and
asks, etc., and then prints out a bank of useful information about XSigma 
values and related.

strangle_stu.py is designed to be opened and initialized directly in an IDE or
editor and will run in terminal window. There is adequate internal 
documentation about how the program works but the user must be thoroughly 
familiar with how strangles work. This version is designed to be used with 
the finutil_stu utility file. finutil_stu must either reside in the same
directory as strangle_stu or have strangle_stu must have a path command 
pointing to the folder that holds finutil_stu.

Before strangle_stu is attempted, the user must get a one-year and 30-day
estimator for historical volatility, presumably using a program like hvmaster.
The user must also have access to bids and asks for the calls and puts used
in the strangle, plus either the expiry date or days to expiry.

Aside from this, the documentation in the program largely speaks for itself.