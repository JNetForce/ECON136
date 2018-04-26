# callidvexstu.py (modified from callidv) in PyGo\PyFiTeach, Python 3
# This is the BSM (old) IDV model for calls only, modified to calculate days to expiry.
# This model accepts interest rates.
# This is the student version of the model and is not the master. The master
# for this model will always be PyGo\PyFi\callidvex.py
# This model uses the "divide and conquer" iteration.
# Version 3.1 Dated February 25, 2018   Prof Gary Evans
# 
# Because this model takes today's date to make expiry calculations, default values
# loaded with this model WILL NOT WORK.
#
import math
import time
from datetime import date
#
# User-provided date:
#
stosym = "wmt"
exyear = int(2018)
exmonth = int(3)
exday = int (16)
stopr = float(92.80)
strike = float(94.00)
callBid = float(1.02)
callAsk = float(1.04)
rfir = float (0.0225)
#
#  Initialize key variables below
#
daystd = int(1)
cipd = float(0.00)
d1 = float(0.0)
durvol = float(0.0)
cumd1 = float(0.0)
cumd2 = float(0.0)
newcp = float (0.0)
tempcp = float(0.0)                                                                                                                                                                                                                                                                                        
timedecay = float (0.0)
tdprice = float (0.0)
callpr = float(0.0)
#
# Calculating strike value (PEG), which is somewhere between BB and BA. 
# PEG coefficient is explained in lecture.
peg_coef = 0.60
spread = callAsk - callBid
callpr = callBid + (peg_coef*spread)
# Calculating days to expiry:
tnow = date.today()
expiry = date(exyear, exmonth, exday)
days2expiry = abs(expiry - tnow)
days = int(days2expiry.days)
#  Our method for calculating the cumulative standard normal distribution:
def csnd(dval):
	return (1.0 + math.erf(dval/math.sqrt(2.0)))/2.0
#	
#  Below we calculate implied daily volatility using a recursive method to
#  converge to an answer.  First we make an initializing calculation, then 
#  we converge inside the while loop. The convergence method shown is Prof E's
#  "Divide and Conquer", which is relatively efficient, usually using only 8
#  (+/- 2) steps. The student should recognize that the cumd1 is the delta.
#  The implied daily volatility that we are seeking is "cipd" below.
#
target = callpr
precision = float(1e-4)
count = 0
low = 0.0
high = 1.0
cipd = float((high+low)/2)
d1 = math.log(stopr/strike)+((rfir/365)+(cipd**2)/2)*days
durvol = cipd*math.sqrt(days)
cumd1 = csnd(d1/durvol)
cumd2 = csnd((d1/durvol) - durvol)
discount = math.exp(-rfir*days/365)
tempcp = (stopr*cumd1)-(strike*discount*cumd2)
while tempcp<=(target-precision) or tempcp>=(target+precision):
	if tempcp >= (target+precision):
		high = cipd
	else: 
		low = cipd
	cipd = float((high+low)/2)
	d1 = math.log(stopr/strike)+((rfir/365)+(cipd**2)/2)*days
	durvol = cipd*math.sqrt(days)
	cumd1 = csnd(d1/durvol)
	cumd2 = csnd((d1/durvol) - durvol)
	discount = math.exp(-rfir*days/365)
	tempcp = (stopr*cumd1)-(strike*discount*cumd2)
	count +=1
#
#	Below we calculate one day time decay using our new value for volatility
#   Possible BUG: This may not work if there is only one day left!! 
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
print ( "")
print ( "Date: ", tnow.strftime("%a %b %d %Y"))
print ( "Days to expiry: ", days2expiry.days	)
print ( "Stock price: ", "%.2f" % stopr)
print ( "Strike price: ", "%.2f" % strike)
print ( "Call ASK: ", "%.3f" % callAsk)
print ( "Call BID: ", "%.3f" % callBid)
print ( "Call price (PEG): ", "%.3f" % callpr)
print ( "The Delta:", "%.4f" % cumd1)
print ( "One day time decay:", "%.3f" % timedecay)
print ( "The call's implied volatility: ", "%.5f" % cipd)





