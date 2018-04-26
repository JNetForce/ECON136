# This is the utility file op_util that begins with HW6.
# It includes various utilities, including options pricing
# calculators that we can call with main programs.
# Version 1.2 dated March 6, 2018
# Prof. Evans
#
import math
import time
from datetime import date
#
#  This is how you calc the standard normal dist in Py for dval
def csnd(dval):
	return (1.0 + math.erf(dval/math.sqrt(2.0)))/2.0
#
#
# Calculating days to expiry:
def days2exp(exyear, exmonth, exday):
	tnow = date.today()
	expiry = date(exyear, exmonth, exday)
	days2expiry = abs(expiry - tnow)
	return (int(days2expiry.days))
#
#
# Calculating the BSM call option price.
def copo(stock,strike,dayvol,days,rfir):
	d1 = math.log(stock/strike)+((rfir/365)+(dayvol**2)/2)*days
	durvol = dayvol*math.sqrt(days)
	delta = csnd(d1/durvol)
	cumd2 = csnd((d1/durvol) - durvol)
	discount = math.exp(-rfir*days/365)
	callpr = (stock*delta)-(strike*discount*cumd2)
	return [callpr,delta,durvol]
#
# Calculating the BSM put option price.
def popo(stock,strike,dayvol,days,rfir):
	d1 = math.log(stock/strike)+((rfir/365)+(dayvol**2)/2)*days
	durvol = dayvol*math.sqrt(days)
	delta = csnd(-d1/durvol)
	cumd2 = csnd(-(d1/durvol - durvol))
	discount = math.exp(-rfir*days/365)
	putpr = -(stock*delta)+(strike*discount*cumd2)
	return [putpr,delta,durvol]
#