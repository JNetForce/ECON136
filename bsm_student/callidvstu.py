# callidvstu.py (modified from callidv) in PyGo\PyFiTeach, Python 3
# This is the BSM (old) IDV model for calls only.
# This version does not calculate days to maturity using current date and expiry.
# In this version the user feeds in days.
# Use callidvexstu.py for auto-calculation of days to expiry.
# This is the student version of the model and is not the master. The master
# for this model will always be PyGo\PyFi\callidv.py
# This model uses a primitive iteration technique.
# Version 1.4 Dated February 25, 2018   Prof Gary Evans
#
import math
stosym = "SMPL"
#
# User-provided date:
# Student must decide what value is used for callpr.
#
opchain = "Mar 2 18"
stopr = float(80.00)
strike = float(84.00)
callpr = float(2.122)
rfir = float (0.000)
days = int(4)
# daystd is the number of days to calculate time decay, default: 1.
daystd = int(1)
#
#  Initialize key variables below
#  (This is not actually required. This is your Prof's habit).
cipd = float(0.00)
d1 = float(0)
durvol = float(0) 
cumd1 = float(0)
cumd2 = float(0)
newcp = float (0)
tempcp = float(0)
timedecay = float (0)
tdprice = float (0)
#
#  Our method for calculating the cumulative standard normal distribution:
def csnd(dval):
	return (1.0 + math.erf(dval/math.sqrt(2.0)))/2.0
#	
#  Below we calculate implied daily volatility using a primitive counter.
#  The implied daily volatility that we are seeking is "cipd" below.
#  The student should recognize that the cumd1 is the delta.
#
while tempcp < callpr:
	cipd = cipd + 0.00001
	d1 = math.log(stopr/strike)+((rfir/365)+(cipd**2)/2)*days
	durvol = cipd*math.sqrt(days)
	cumd1 = csnd(d1/durvol)
	cumd2 = csnd((d1/durvol) - durvol)
	discount = math.exp(-rfir*days/365)
	tempcp = (stopr*cumd1)-(strike*discount*cumd2)
#
#  Below we calculate one day time decay using our new value for volatility
#
days = days - daystd
d1 = math.log(stopr/strike)+((rfir/365)+(cipd**2)/2)*days
durvol = cipd*math.sqrt(days)
cumd1 = csnd(d1/durvol)
cumd2 = csnd((d1/durvol) - durvol)
discount = math.exp(-rfir*days/365)
newcp = (stopr*cumd1)-(strike*discount*cumd2)
timedecay = callpr - newcp
#
#  Print results (using the old [pre 3.5 Python] methods).
#
print ("")
print ("CALL")
print ("Stock: ", stosym )
print ("Option chain: ", opchain )
print ("Days to expiry: ", days + 1 )
print ("Stock price: ", "%.3f" % stopr)
print ("Strike price: ", "%.3f" % strike)
print ("Call price: ", "%.3f" % callpr)
print ("The Delta is:", "%.4f" % cumd1)
print ("The call's implied volatility is: ", "%.5f" % cipd)
print ("One day time decay:", "%.3f" % timedecay)



