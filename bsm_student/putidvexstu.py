# putidvexstu.py (modified from putidv) in PyGo\PyFiTeach, Python 3
# This is the BSM (old) IDV model for calls only, modified to calculate days to expiry.
# This model accepts interest rates.
# This is the student version of the model and is not the master. The master
# for this model will always be PyGo\PyFi\putidvex.py
# This model uses the "divide and conquer" iteration.
# Version 3.2 Dated April 6, 2018   Prof Gary Evans
# 
# Because this model takes today's date to make expiry calculations, default values
# loaded with this model WILL NOT WORK.
#
import math
import time
from datetime import date
stosym = "DBX"
exmonth = int(4)
exday = int (20)
stopr = float(30.21)
strike = float(30.00)
putBid = float(1.55)
putAsk = float(1.75)
rfir = float (0.0250)
#
#  Initialize key variables below
#  (This is not actually required. This is your Prof's habit).
#
daystd = int(1)
pidv = float(0.0)
d1 = float(0.0)
durvol = float(0.0)
cumd1 = float(0.0)
cumd2 = float(0.0)
discount = float(0.0)
count = int(0.0)
newpp = float (0.0)
temppp = float(0.0)
timedecay = float (0.0)
tdprice = float (0.0)
putpr = float(0.0)
#
# Calculating strike value (PEG)
spread = putAsk - putBid
putpr = putBid + ((0.6)*spread)
# Calculating days to expiry:
tnow = date.today()
expiry = date(tnow.year, exmonth, exday)
days2expiry = abs(expiry - tnow)
days = int(days2expiry.days)
#  This is how you calc the standard normal dist in Py for dval
def csnd(dval):
	return (1.0 + math.erf(dval/math.sqrt(2.0)))/2.0
#
while temppp < putpr:
	pidv = pidv + 0.00001
	d1 = math.log(stopr/strike)+((rfir/365)+(pidv**2)/2)*days
	durvol = pidv*math.sqrt(days)
	cumd1 = csnd(-d1/durvol)
	cumd2 = csnd(-(d1/durvol - durvol))
	discount = math.exp(-rfir*days/365)
	temppp = -(stopr*cumd1)+(strike*discount*cumd2)
#
#	Below we calculate one day time decay using our new value for volatility
#
#   NOTE: This has a bug that you teacher did not have time to fix. It won't 
#   calculate time decay if expiration is tomorrow. It tries to divide by zero!
#
days = days - daystd
d1 = math.log(stopr/strike)+((rfir/365)+(pidv**2)/2)*days
durvol = pidv*math.sqrt(days)
cumd1 = csnd(-d1/durvol)
cumd2 = csnd(-(d1/durvol - durvol))
discount = math.exp(-rfir*days/365)
newpp = -(stopr*cumd1)+(strike*discount*cumd2)
timedecay = putpr - newpp	
#
print ("")
print ("Date: ", tnow.strftime("%a %b %d %Y"))
print ("PUT" , stosym , expiry.strftime("%b %d"))
print ("Stock price: ", "%.3f" % stopr)
print ("Strike price: ", "%.2f" % strike)
print ("Days to expiry: ", days2expiry.days	)
print ("Put ASK: ", "%.3f" % putAsk)
print ("Put BID: ", "%.3f" % putBid)
print ("Put price (PEG): ", "%.3f" % putpr)
print ("The Delta:", "%.5f" % cumd1)
print ("One day time decay:", "%.3f" % timedecay)
print ("The put's implied volatility: ", "%.5f" % pidv)
#




