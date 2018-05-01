using SpecialFunctions

# from datetime import date
# User-provided date:
#
stosym = "wmt"
exyear = 2019
exmonth = 5
exday = 16
stopr = 92.68
strike = 94
callBid = 0.97
callAsk = 1.01
rfir = 0.0225
#
#  Initialize key variables below
#  (This is not actually required. This is your Prof's habit).
#
daystd = 1
cipd = 0.0
d1 = 0.0
durvol = 0.0
cumd1 = 0.0
cumd2 = 0.0
newcp = 0.0
tempcp = 0.0
timedecay = 0.0
tdprice = 0.0
callpr = 0.0
#
# Calculating strike value (PEG), which is somewhere between BB and BA.
# PEG coefficient is explained in lecture.
peg_coef = 0.60
spread = callAsk - callBid
callpr = callBid + (peg_coef*spread)
# Calculating days to expiry:
tnow = Dates.today()
expiry = Dates.Date(exyear, exmonth, exday)
days = Int(expiry - tnow)
#  Our method for calculating the cumulative standard normal distribution:
function csnd(dval)
	return (1.0 + erf(dval/sqrt(2.0)))/2.0
end
#
#  Below we calculate implied daily volatility using a recursive method to
#  converge to an answer.  First we make an initializing calculation, then
#  we converge inside the while loop. The convergence method shown is Prof E's
#  "Divide and Conquer", which is relatively efficient, usually using only 8
#  (+/- 2) steps. The student should recognize that the cumd1 is the delta.
#  The implied daily volatility that we are seeking is "cipd" below.
#
target = callpr
precision = 1e-4
count = 0
low = 0.0
high = 1.0
cipd = (high+low)/2
d1 = log(stopr/strike)+((rfir/365)+(cipd^2)/2)*days
durvol = cipd*sqrt(days)
cumd1 = csnd(-d1/durvol)
cumd2 = csnd(-(d1/durvol - durvol))
discount = exp(-rfir*days/365)
tempcp = -(stopr*cumd1)+(strike*discount*cumd2)
while tempcp<=(target-precision) || tempcp>=(target+precision)
	if tempcp >= (target+precision)
		high = cipd
	else
		low = cipd
    end
	cipd = (high+low)/2
	d1 = log(stopr/strike)+((rfir/365)+(cipd^2)/2)*days
	durvol = cipd*sqrt(days)
	cumd1 = csnd(-d1/durvol)
	cumd2 = csnd(-(d1/durvol - durvol))
	discount = exp(-rfir*days/365)
	tempcp = -(stopr*cumd1)+(strike*discount*cumd2)
	count +=1
end
#	Below we calculate one day time decay using our new value for volatility
days = days - daystd
d1 = log(stopr/strike)+((rfir/365)+(cipd^2)/2)*days
durvol = cipd*sqrt(days)
cumd1 = csnd(-d1/durvol)
cumd2 = csnd(-(d1/durvol - durvol))
discount = exp(-rfir*days/365)
newcp = -(stopr*cumd1)+(strike*discount*cumd2)
timedecay = callpr - newcp
#
#  Print results (using the old [pre 3.5 Python] methods).
#
println( "")
# print ( "Date: ", tnow.strftime("%a %b %d %Y"))
println( "Days to expiry: ", days)
println( "Stock price: ", stopr)
println( "Strike price: ", strike)
println( "Call ASK: ", callAsk)
println( "Call BID: ", callBid)
println( "Call price (PEG): ", callpr)
println( "The Delta:", cumd1)
println( "One day time decay:", timedecay)
println( "The call's implied volatility: ", cipd)
