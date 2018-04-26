This zip file has 8 versions of the Black-Scholes-Merton modified options
used by Prof Evans in Economics 136. All of the files are modified from 
traditional BSM to use and calculate DAILY VOLATILITY rather than annual 
volatility.
This package was created on April 6, 2018. Here are the models:

op.util.py - a utility file that holds the methods for calculating call
option price or put option put option price using BSM. This utility is 
called by a program with the data that you need to use. This utility file
must be in the same file as the main program that calls it unless a path
command in added.

cop_main.py - This is the elementary call option pricing model used to solve
for the call's price using user estimate for daily volatility. This calls 
copo from the op.util.py folder.

pop_main.py - This is the elementary put option pricing model used to solve
for the put's price using user estimate for daily volatility. This calls 
popo from the op.util.py folder.

option_calc.py - This is a large program that calculates a full range of call
or put prices or their deltas from a range of strike prices for multiple
expiries. This program draws upon the utilities in op.util.py.

callidvstu.py - This is an elementary program for calculating call idv if 
the call price is known. User must provide days to expiry and the call price.

putidvstu.py - This is an elementary program for calculating put idv if 
the call price is known. User must provide days to expiry and the put price.

callidvexstu.py - This is the advanced model for calculating call idv. The
user must provide current bid and ask and the expiry date. This version is
designed to be modified for an API algo. The model uses divide and conquer
for convergence. THIS MODEL WILL NOT WORK WITH DEFAULT VALUES!

putidvexstu.py - This is the advanced model for calculating put idv. The
user must provide current bid and ask and the expiry date. This version is
designed to be modified for an API algo. The model uses divide and conquer
for convergence. THIS MODEL WILL NOT WORK WITH DEFAULT VALUES!