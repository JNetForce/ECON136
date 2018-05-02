# strangle_stu.py 
#
# This is a MOS model: Mudd Open Source only.
# This is a deep strangle model based upon the Taboga concept (student version).
# Much of the documentation can be found in the core Taboga model or finutil.py
# Designed in Python 3.6 on for Economics 136
# Original version developed on May 30, 2017 by Prof Evans
# This is version 2.1stu, dated April 11, 2017
#

# This model draws upon utility model finutil_stu. That model must either be in
# the same directory as this model or the path command below must be used to
# point to its location.
# import sys
# sys.path.append('c:/Users/Prof Gary Evans/Dropbox/PyGo/PyFi')
import finutil_stu
fu = finutil_stu
# This version calculates IDV for the put and call, but also requires that you 
# supply historical volatility (252 and 30 day). You can include an earnings 
# date if date is relevant. 
#
# Load data
aname = "Prof Evans"
stosym = "MSFT"
tnow = Dates.today()
# Set earnings to True if this is an earnings-based strangle.
earnings = true
# If you don't need to calculate the days to expiry and earnings (optional) 
# then calcdays is False (default). 
calcdays = false
# BEGIN of optional time data. Load below ONLY if calcdays = True
# Expiration date:
exyear = 2018
exmonth = 2
exday = 16
# Earnings date (load only if relevant):
eayear = 2018
eamonth = 1
eaday = 31
# END of optional time data load
#
# This model does not use the alpha.
# stock = 15.15
# callstrike = 16
# callbid = 0.90
# callask = 0.93
# putstrike = 15
# putbid = 1.150
# putask = 1.18
# sigma252 = 0.043534
# sigma30 = 0.025
###########################
stock = 166.86
callstrike = 170
callbid = 3.20
callask = 3.25
putstrike = 165
putbid = 4.50
putask = 4.60
sigma252 = 0.011358
sigma30 = 0.016387
if calcdays
    days = fu.daysto(exyear,exmonth,exday)
    if earnings
        daystoearn = fu.daysto(eayear,eamonth,eaday)
    end
else
    # Here you have to supply the days if you don't calculate them.
    days = 14.0
    if earnings
        daystoearn = 11.0 
    end
end   
#
moname = fu.monthname(exmonth)
# Set effective options prices (PEG)
peg = 0.6
cspread = callask - callbid
callpr = callbid + (peg*cspread)
pspread = putask - putbid
putpr = putbid + (peg*pspread)
cost = callpr + putpr
# Note: callbe and putbe should be calced based upon the prices they would
# have to be the day after earnings, especially for more distant options.
callbe = stock + cost
putbe = stock - cost
callbegr = log(callbe/stock)*100
putbegr = log(putbe/stock)*100
# Consider adding log percent breakeven to current value
#
# Calculate call and put ideal prices based upon historical volatilities.
hv252 = sigma252*fu.durvol(days)
cop252 = fu.otranche(stock,callstrike,hv252,true)
pop252 = fu.otranche(stock,putstrike,hv252,false)
hv30 = sigma30*fu.durvol(days)
cop30 = fu.otranche(stock,callstrike,hv30,true)
pop30 = fu.otranche(stock,putstrike,hv30,false)
#
# Calculate call and put IDV based upon actual prices
# See the documentation for finutil and tabogacidv to see what these are doing.
# Start with the call:
#
seedsigma = 1e-6
cutoff = 1e-4
tempop = 0.00
price2 = 0.00
derive = 0.00
cdurseed = seedsigma*fu.durvol(days)
cdaysigma = 0.06
cdursigma = cdaysigma*fu.durvol(days)
#
# The convergence shown here (Newton's method) was designed by Alec Griffith '17 
#
while abs(tempop - callpr) > cutoff
    tempop = fu.otranche(stock,callstrike,cdursigma,true)
    price2 = fu.otranche(stock,callstrike,cdursigma+cdurseed,true)
    deriv = (price2-tempop)/seedsigma
    cdaysigma -= (tempop-callpr)/deriv
    cdursigma = cdaysigma*fu.durvol(days)
end
# End of Loop!
#
# Repeat for the put:
#
seedsigma = 1e-6
cutoff = 1e-4
tempop = 0.00
price2 = 0.00
derive = 0.00
pdurseed = seedsigma*fu.durvol(days)
pdaysigma = 0.01
pdursigma = pdaysigma*fu.durvol(days)
call = false
#
#
while abs(tempop - putpr) > cutoff
    tempop = fu.otranche(stock,putstrike,pdursigma,false)
    price2 = fu.otranche(stock,putstrike,pdursigma+pdurseed,false)
    deriv = (price2-tempop)/seedsigma
    pdaysigma -= (tempop-putpr)/deriv
    pdursigma = pdaysigma*fu.durvol(days)
end
# End of Loop!
callsigmaratio = cdaysigma/sigma252
putsigmaratio = pdaysigma/sigma252
#
dateString = Dates.format(now(), "e u d y")
println()
println("Strangle Model")
println("Analyst's name: $(aname)")
println( "Date: $(dateString)")
println( "Stock symbol: $(stosym)")
println("Option chain: $(moname), $(exday)")
println("Days to expiry: $(days)")
println( "Stock price: $(stock)")
println( "Call strike price: $(callstrike)")
println( "Call Bid: $(callbid)")
println( "Call Ask: $(callask)")
println( "Call price: $(callpr)")
println( "Put strike price: $(putstrike)")
println( "Put Bid: $(putbid)")
println( "Put Ask: $(putask)")
println( "Put price: $(putpr)")
println( "Position cost: $(cost)")
if earnings
    println("Days to earnings: $(daystoearn)")
println( "Call breakeven price: $(callbe)")
println( "Call breakeven ln percent: $(callbegr)")
println( "Put breakeven price: $(putbe)")
println( "Put breakeven ln percent: $(putbegr)")
println( "Call value based upon 252-day HV ($(sigma252)) : $(cop252)")
println( "Call value based upon 30-day HV ($(sigma30)) : $(cop30)")
println( "Put value based upon 252-day HV ($(sigma252)) : $(pop252)")
println( "Put value based upon 30-day HV ($(sigma30)) : $(pop30)")
println( "Call implied duration volatility: $(cdursigma)")
println( "Put implied duration volatility: $(pdursigma)")
println("CRITICAL")
println( "Call implied daily volatility: $(cdaysigma)")
println( "Put implied daily volatility: $(pdaysigma)")
println( "Call sigma ratio: $(callsigmaratio)")
println( "Put sigma ratio: $(putsigmaratio)")
#
# Calculate one day time decay using our calculated IDV.
#
if days >= 2.0
    days = days - 1.0
    cdursigma = cdaysigma*fu.durvol(days)
    cprice1d = fu.otranche(stock,callstrike,cdursigma,true)
    pdursigma = pdaysigma*fu.durvol(days)
    pprice1d = fu.otranche(stock,putstrike,pdursigma,false)
    timedecay = (callpr - cprice1d) + (putpr - pprice1d)
    println( "One day time decay: $(timedecay)")
else
    println( "No time decay with one day remaining.")
end
end
#