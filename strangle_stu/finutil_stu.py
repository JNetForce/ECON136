# This is finutil_stu.py, residing typically in \PyGo\PyTeach
# This is a frozen and reduced version of finutil.py. This file is not likely
# to be current with funutil and should not be used in place of finutil (see log).
# This should only be used with models with the _stu appendage.
# These are the utilities that are used throughout the various financial models
# for such things as calculating options prices and volatilities. These are 
# designed to be used with Version 3.6 of Python.
# This version 1.2stu, April 11, 2018  NOTE: This version has not been completely 
# tested.
# Maintained by Professor Evans
#
import math
from datetime import date
import numpy as np
# 
# daysto calculates the number of days between now and some event, such as days2expiry
# as an integer float.
#
def daysto(eyear,emonth,eday):
	tnow = date.today()
	expiry = date(eyear, emonth, eday)
	days2expiry = abs(expiry - tnow)
	
	return float(days2expiry.days)
#
def monthname(mo):
    mo = mo - 1
    monthlabel = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG',
                 'SEP', 'OCT', 'NOV', 'DEC' ]
    return monthlabel[mo]
#
# csnd integrates a standard normal distribution up to some sigma.
# 
def csnd(point): 
	return (1.0 + math.erf(point/math.sqrt(2.0)))/2.0
#
# cnd integrates a Gaussian distribution up to some value.
#
def cnd(center,point,stdev):
	return (1.0 + math.erf((point - center)/(stdev*math.sqrt(2.0))))/2.0
#
# Calculating the BSM call option price, traditional model. This requires the
# user to provide stock price, strike price, daily volatility, risk-free interest
# rate and days to expiry. (To calculate days use method daysto above).
# This returns the call price, the delta, and duration volatility as a tuple 
# array. See popo below for puts.
#
def copo(stock,strike,dayvol,days,rfir):
	d1 = math.log(stock/strike)+((rfir/365)+(dayvol**2)/2)*days
	durvol = dayvol*math.sqrt(days)
	delta = csnd(d1/durvol)
	cumd2 = csnd((d1/durvol) - durvol)
	discount = math.exp(-rfir*days/365)
	callpr = (stock*delta)-(strike*discount*cumd2)
	return [callpr,delta,durvol]
#
# An elementary function for calculating the stock price adjusted for drift.
#
def drift(alpha,time):
	return 1.0*math.exp(alpha*time)
#
# An elementary multiplier function for converting daily volatility to duration
# volatility.
#
def durvol(time):
	return 1.0*math.sqrt(time)
#
# An elementary price expected-mean-value adjustment multiplier for log 
# distributed prices. The mean of a log-distributed pdf is adjusted by minus 
# one-half variance.
#
def lnmeanshift(sigma):
	return 1.0*math.exp(-1.0*(sigma*sigma/2))
#
# A time-discount function to discount the value of a future payment (like an 
# option) discounted at the risk-free interest rate. The variable riskfreerate 
# is annual and time is in days.
#
def dcount(riskfreerate,time):
	return 1.0*math.exp(-1.0*(riskfreerate/365)*time)
#
# This is an option tranche value calculator function that assumes you have a 
# stock price and strike price, adjusted externally (for example, drift is 
# adjusted with drift above). This will calculate the strike-price adjusted 
# tranche from either -5 sigma to the strike or from the strike to +5 sigma. 
# Sigma used here is duration sigma, adjusted outside using durvol above.
# Main program must set call to true if a call, false if a put.
#
def otranche(stock,strike,dursigma,call):
	sspread = (math.log(strike/stock))/dursigma
	if call:
		binborder = np.linspace(sspread, 5.00, num=24, dtype=float)
	else:
		binborder = np.linspace(-5.0, sspread, num=24, dtype=float)
	size = len(binborder)
	binedgeprob = np.zeros(size) 
#	
	for i in range(0,size):
		binedgeprob[i] = csnd(binborder[i])
	size = size - 1
	binprob = np.zeros(size)
	binmidprice = np.zeros(size)
	binvalue = np.zeros(size)
#
	for i in range(0,size): 
		binprob[i] = binedgeprob[i+1] - binedgeprob[i]
		binmidprice[i] = ((stock*math.exp(((binborder[i+1]+binborder[i])/2.0)
        *dursigma))*lnmeanshift(dursigma)) - strike
		binvalue[i] = binmidprice[i]*binprob[i]
#
	if call:
		optionprice = np.sum(binvalue[0:(i+1)])
	else:
		optionprice = (np.sum(binvalue[0:(i+1)]))*-1.0
#	
	return optionprice
#
# This is full tranche value calculator function that assumes you have a stock 
# price and reference price, usually a strike price (and still called that 
# here). This will calculate the tranche value from either -5 sigma to the 
# reference price (left is true) or from the reference to +5 sigma (left 
# is false). This is similar to otranche except that it does not subtract the 
# strike price and therefore gives the full value of the tranche. It is 
# designed to be used primarily by the Aruba Model to calculate the value of 
# the remaining stock tranche if the covered call you wrote has been exercised.
#
def ftranche(stock,strike,sigma,left):
	sspread = (math.log(strike/stock))/sigma
	if left:
		binborder = np.linspace(-5.0, sspread, num=24, dtype=float)
	else:		
		binborder = np.linspace(sspread, 5.00, num=24, dtype=float)
	size = len(binborder)
	binedgeprob = np.zeros(size) 
#	
	for i in range(0,size):
		binedgeprob[i] = csnd(binborder[i])
	size = size - 1
	binprob = np.zeros(size)
	binmidprice = np.zeros(size)
	binvalue = np.zeros(size)
#
	for i in range(0,size): 
		binprob[i] = binedgeprob[i+1] - binedgeprob[i]
		binmidprice[i] = ((stock*math.exp(((binborder[i+1]+binborder[i])/2.0)
        *sigma))*lnmeanshift(sigma))
		binvalue[i] = binmidprice[i]*binprob[i]
#
	trancheprice = np.sum(binvalue[0:(i+1)])
	return trancheprice
#
# oidv calculates implied daily and duration volatility for a call or a put
# using divide and conquer (the default for most models). Also see oidvnm.
# This uses an iterative process that uses otranche (above) to calculate the 
# sigma, here an implied sigma, from the existing option value (ovalue).
# The call variable is True for a call, False for a put. The convergence is 
# within the while loop. This function returns a tuple of two values, daily 
# IDV and duration IDV. 
#
def oidv(stock,strike,ovalue,days,call):
    precision = float(1e-4)
    low = 0.0
    high = 1.0
    daysigma = float((high+low)/2)
    dursigma = daysigma*durvol(days)
    tempop = otranche(stock,strike,dursigma,call)
    while tempop<=(ovalue-precision) or tempop>=(ovalue+precision):
        if tempop >= (ovalue+precision):
            high = daysigma
        else: 
            low = daysigma
        daysigma = float((high+low)/2)
        dursigma = daysigma*durvol(days)
        tempop = otranche(stock,strike,dursigma,call)
    # End of Loop!
    return [daysigma,dursigma]   
#
# oidvnm calculates implied daily and duration volatility for a call or a put
# using Newton's Method for convergence (default is divide and conquer).
# This uses an iterative process that uses otranche (above) to calculate the 
# sigma, here an implied sigma, from the existing option value (ovalue).
# The call variable is True for a call, False for a put. The convergence is 
# within the while loop. This function returns a tuple of two values, daily 
# IDV and duration IDV. 
#
def oidvnm(stock,strike,ovalue,days,call):
	seedsigma = 1e-6
	durseed = seedsigma*durvol(days)
	# NOTE: daysigma is supposed to be set at a reasonable estimate of the 
    # actual idv. The Newton method can explode if it is not (especially if you
    # enter option price, strike, and value data that are very unrealistic).
	# Consider setting daysigma at sqrt*time*ln(strike/stock). It was 
    # originally set at 0.05
	daysigma = (math.log(strike/stock))*math.sqrt(days)
	dursigma = daysigma*durvol(days)
	cutoff = 1e-4
	tempop = float(0.00)
	#
	# The loop starts here. You start with a test sigma and converge to the 
    # actual sigma. The convergence shown here (Newton's method) was designed 
    # by Alec Griffith '17 
	#
	while np.abs(tempop - ovalue) > cutoff:
		tempop = otranche(stock,strike,dursigma,call)
		price2 = otranche(stock,strike,dursigma+durseed,call)
		deriv = (price2-tempop)/seedsigma
		daysigma -= (tempop-ovalue)/deriv
		dursigma = daysigma*durvol(days)
	# End of Loop!
	return [daysigma,dursigma]
#
# Calculating the BSM put option price, traditional model. This requires the
# user to provide stock price, strike price, daily volatility, risk-free interest
# rate and days to expiry. (To calculate days use method daysto above).
# This returns the put price, the delta, and duration volatility as a tuple 
# array. See copo below for calls.
#
def popo(stock,strike,dayvol,days,rfir):
	d1 = math.log(stock/strike)+((rfir/365)+(dayvol**2)/2)*days
	durvol = dayvol*math.sqrt(days)
	delta = csnd(-d1/durvol)
	cumd2 = csnd(-(d1/durvol - durvol))
	discount = math.exp(-rfir*days/365)
	putpr = -(stock*delta)+(strike*discount*cumd2)
	return [putpr,delta,durvol]
#
# tdfecay adds an extension to the otranche calculator (Taboga model)	
# to calculate one-day time decay.
#
	
def tdecay(stock, strike, daysigma, oprice, days, call):
	days = days - 1.0
	dursigma = daysigma*durvol(days)
	oprice1d = otranche(stock,strike,dursigma,call)
	timedecay = oprice - oprice1d
	return timedecay