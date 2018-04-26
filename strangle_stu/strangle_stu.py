# strangle_stu.py 
#
# This is a MOS model: Mudd Open Source only.
# This is a deep strangle model based upon the Taboga concept (student version).
# Much of the documentation can be found in the core Taboga model or finutil.py
# Designed in Python 3.6 on for Economics 136
# Original version developed on May 30, 2017 by Prof Evans
# This is version 2.1stu, dated April 11, 2017
#
import math
import numpy as np
from datetime import date
# This model draws upon utility model finutil_stu. That model must either be in
# the same directory as this model or the path command below must be used to
# point to its location.
# import sys
# sys.path.append('c:/Users/Prof Gary Evans/Dropbox/PyGo/PyFi')
import finutil_stu as fu
# This version calculates IDV for the put and call, but also requires that you 
# supply historical volatility (252 and 30 day). You can include an earnings 
# date if date is relevant. 
#
# Load data
aname = "Prof Evans"
stosym = "MSFT"
tnow = date.today()
# Set earnings to True if this is an earnings-based strangle.
earnings = True
# If you don't need to calculate the days to expiry and earnings (optional) 
# then calcdays is False (default). 
calcdays = False
# BEGIN of optional time data. Load below ONLY if calcdays = True
# Expiration date:
exyear = int(2018)
exmonth = int(2)
exday = int (16)
# Earnings date (load only if relevant):
eayear = int(2018)
eamonth = int(1)
eaday = int (31)
# END of optional time data load
#
# This model does not use the alpha.
# stock = float(15.15)
# callstrike = float(16)
# callbid = float(0.90)
# callask = float (0.93)
# putstrike = float(15)
# putbid = float(1.150)
# putask = float(1.18)
# sigma252 = float(0.043534)
# sigma30 = float(0.025)
###########################
stock = float(166.86)
callstrike = float(170)
callbid = float(3.20)
callask = float (3.25)
putstrike = float(165)
putbid = float(4.50)
putask = float(4.60)
sigma252 = float(0.011358)
sigma30 = float(0.016387)
if calcdays:
	days = fu.daysto(exyear,exmonth,exday)
	if earnings:
		daystoearn = fu.daysto(eayear,eamonth,eaday)
else:
	# Here you have to supply the days if you don't calculate them.
	days = float(14.0)
	if earnings:
		daystoearn = float(11.0)	
#
moname = str(fu.monthname(exmonth))
# Set effective options prices (PEG)
peg = float(0.6)
cspread = callask - callbid
callpr = callbid + (peg*cspread)
pspread = putask - putbid
putpr = putbid + (peg*pspread)
cost = callpr + putpr
# Note: callbe and putbe should be calced based upon the prices they would
# have to be the day after earnings, especially for more distant options.
callbe = stock + cost
putbe = stock - cost
callbegr = math.log(callbe/stock)*100
putbegr = math.log(putbe/stock)*100
# Consider adding log percent breakeven to current value
#
# Calculate call and put ideal prices based upon historical volatilities.
hv252 = sigma252*fu.durvol(days)
cop252 = fu.otranche(stock,callstrike,hv252,True)
pop252 = fu.otranche(stock,putstrike,hv252,False)
hv30 = sigma30*fu.durvol(days)
cop30 = fu.otranche(stock,callstrike,hv30,True)
pop30 = fu.otranche(stock,putstrike,hv30,False)
#
# Calculate call and put IDV based upon actual prices
# See the documentation for finutil and tabogacidv to see what these are doing.
# Start with the call:
#
seedsigma = 1e-6
cutoff = 1e-4
tempop = float(0.00)
price2 = float(0.00)
derive = float(0.00)
cdurseed = seedsigma*fu.durvol(days)
cdaysigma = 0.06
cdursigma = cdaysigma*fu.durvol(days)
#
# The convergence shown here (Newton's method) was designed by Alec Griffith '17 
#
while np.abs(tempop - callpr) > cutoff:
	tempop = fu.otranche(stock,callstrike,cdursigma,True)
	price2 = fu.otranche(stock,callstrike,cdursigma+cdurseed,True)
	deriv = (price2-tempop)/seedsigma
	cdaysigma -= (tempop-callpr)/deriv
	cdursigma = cdaysigma*fu.durvol(days)
# End of Loop!
#
# Repeat for the put:
#
seedsigma = 1e-6
cutoff = 1e-4
tempop = float(0.00)
price2 = float(0.00)
derive = float(0.00)
pdurseed = seedsigma*fu.durvol(days)
pdaysigma = 0.01
pdursigma = pdaysigma*fu.durvol(days)
call = False
#
#
while np.abs(tempop - putpr) > cutoff:
	tempop = fu.otranche(stock,putstrike,pdursigma,False)
	price2 = fu.otranche(stock,putstrike,pdursigma+pdurseed,False)
	deriv = (price2-tempop)/seedsigma
	pdaysigma -= (tempop-putpr)/deriv
	pdursigma = pdaysigma*fu.durvol(days)
# End of Loop!
callsigmaratio = cdaysigma/sigma252
putsigmaratio = pdaysigma/sigma252
#
print ()
print ("Strangle Model")
print ("Analyst's name: ", aname)
print ( "Date: ", tnow.strftime("%a %b %d %Y"))
print ( "Stock symbol: ", stosym)
print ("Option chain: ", moname, exday)
print ("Days to expiry: ", '{:.1f}'.format(days))
print ( "Stock price: ", "%.2f" % stock)
print ( "Call strike price: ", "%.3f" % callstrike)
print ( "Call Bid: ", "%.3f" % callbid)
print ( "Call Ask: ", "%.3f" % callask)
print ( "Call price: ", "%.3f" % callpr)
print ( "Put strike price: ", "%.3f" % putstrike)
print ( "Put Bid: ", "%.3f" % putbid)
print ( "Put Ask: ", "%.3f" % putask)
print ( "Put price: ", "%.3f" % putpr)
print ( "Position cost: ", '{:.2f}'.format(cost))
if earnings:
	print ("Days to earnings: ", '{:.1f}'.format(daystoearn))
print ( "Call breakeven price: ", '{:.2f}'.format(callbe))
print ( "Call breakeven ln percent: ", '{:.3f}'.format(callbegr))
print ( "Put breakeven price: ", '{:.2f}'.format(putbe))
print ( "Put breakeven ln percent: ", '{:.3f}'.format(putbegr))
print ( "Call value based upon 252-day HV (", "%.6f" % sigma252,") : ","%.4f" % cop252)
print ( "Call value based upon 30-day HV (", "%.6f" % sigma30,") : ","%.4f" % cop30)
print ( "Put value based upon 252-day HV (", "%.6f" % sigma252,") : ","%.4f" % pop252)
print ( "Put value based upon 30-day HV (", "%.6f" % sigma30,") : ","%.4f" % pop30)
print ( "Call implied duration volatility: ", "%.5f" % cdursigma)
print ( "Put implied duration volatility: ", "%.5f" % pdursigma)
print ("CRITICAL")
print ( "Call implied daily volatility: ", "%.5f" % cdaysigma)
print ( "Put implied daily volatility: ", "%.5f" % pdaysigma)
print ( "Call sigma ratio: ", "%.4f" % callsigmaratio)
print ( "Put sigma ratio: ", "%.4f" % putsigmaratio)
#
# Calculate one day time decay using our calculated IDV.
#
if days >= 2.0:
	days = days - 1.0
	cdursigma = cdaysigma*fu.durvol(days)
	cprice1d = fu.otranche(stock,callstrike,cdursigma,True)
	pdursigma = pdaysigma*fu.durvol(days)
	pprice1d = fu.otranche(stock,putstrike,pdursigma,False)
	timedecay = (callpr - cprice1d) + (putpr - pprice1d)
	print ( "One day time decay: ", "%.3f" % timedecay)
else:
	print ( "No time decay with one day remaining.")
#