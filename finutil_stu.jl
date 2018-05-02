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
# 
# daysto calculates the number of days between now and some event, such as days2expiry
# as an integer float.
#
using SpecialFunctions

function daysto(eyear,emonth,eday)
    tnow = Dates.today()
    expiry = Dates.Date(eyear, emonth, eday)
    days2expiry = abs(expiry - tnow)
    return float(days2expiry.days)
end
#
function monthname(mo)
    monthlabel = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                 "SEP", "OCT", "NOV", "DEC" ]
    return monthlabel[mo]
end
#
# csnd integrates a standard normal distribution up to some sigma.
# 
function csnd(point)
    return (1.0 + erf(point/sqrt(2.0)))/2.0
end
#
# cnd integrates a Gaussian distribution up to some value.
#
function cnd(center,point,stdev)
    return (1.0 + erf((point - center)/(stdev*sqrt(2.0))))/2.0
end
#
# Calculating the BSM call option price, traditional model. This requires the
# user to provide stock price, strike price, daily volatility, risk-free interest
# rate and days to expiry. (To calculate days use method daysto above).
# This returns the call price, the delta, and duration volatility as a tuple 
# array. See popo below for puts.
#
function copo(stock,strike,dayvol,days,rfir)
    d1 = log(stock/strike)+((rfir/365)+(dayvol^2)/2)*days
    durvol = dayvol*sqrt(days)
    delta = csnd(d1/durvol)
    cumd2 = csnd((d1/durvol) - durvol)
    discount = exp(-rfir*days/365)
    callpr = (stock*delta)-(strike*discount*cumd2)
    return [callpr,delta,durvol]
end
#
# An elementary function for calculating the stock price adjusted for drift.
#
function drift(alpha,time)
    return 1.0*exp(alpha*time)
end
#
# An elementary multiplier function for converting daily volatility to duration
# volatility.
#
function durvol(time)
    return 1.0*sqrt(time)
end
#
# An elementary price expected-mean-value adjustment multiplier for log 
# distributed prices. The mean of a log-distributed pdf is adjusted by minus 
# one-half variance.
#
function lnmeanshift(sigma)
    return 1.0*exp(-1.0*(sigma*sigma/2))
end
#
# A time-discount function to discount the value of a future payment (like an 
# option) discounted at the risk-free interest rate. The variable riskfreerate 
# is annual and time is in days.
#
function dcount(riskfreerate,time)
    return 1.0*exp(-1.0*(riskfreerate/365)*time)
end
#
# This is an option tranche value calculator function that assumes you have a 
# stock price and strike price, adjusted externally (for example, drift is 
# adjusted with drift above). This will calculate the strike-price adjusted 
# tranche from either -5 sigma to the strike or from the strike to +5 sigma. 
# Sigma used here is duration sigma, adjusted outside using durvol above.
# Main program must set call to true if a call, false if a put.
#
function otranche(stock,strike,dursigma,call)
    sspread = (log(strike/stock))/dursigma
    if call
        binborder = linspace(sspread, 5.00, 24)
    else
        binborder = linspace(-5.0, sspread, 24)
    end
    num_bins = 24
    binedgeprob = zeros(num_bins) 
#   
    for i = 1:num_bins
        binedgeprob[i] = csnd(binborder[i])
    end
    num_bins = num_bins - 1
    binprob = zeros(num_bins)
    binmidprice = zeros(num_bins)
    binvalue = zeros(num_bins)
#
    for i = 1:num_bins
        binprob[i] = binedgeprob[i+1] - binedgeprob[i]
        binmidprice[i] = ((stock*exp(((binborder[i+1]+binborder[i])/2.0)*dursigma))*lnmeanshift(dursigma)) - strike
        binvalue[i] = binmidprice[i]*binprob[i]
    end
    if call
        optionprice = sum(binvalue)
    else
        optionprice = (sum(binvalue))*-1.0
    end
#   
    return optionprice
end
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
function ftranche(stock,strike,sigma,left)
    sspread = (log(strike/stock))/sigma
    if left
        binborder = linspace(-5.0, sspread, n=24)
    else
        binborder = linspace(sspread, 5.0, n=24)
    end
    num_bins = 24
    binedgeprob = zeros(24) 
#   
    for i = 1:num_bins
        binedgeprob[i] = csnd(binborder[i])
    end
    num_bins = num_bins - 1
    binprob = zeros(num_bins)
    binmidprice = np.zeros(num_bins)
    binvalue = np.zeros(num_bins)
#
    for i = 1:num_bins 
        binprob[i] = binedgeprob[i+1] - binedgeprob[i]
        binmidprice[i] = ((stock*exp(((binborder[i+1]+binborder[i])/2.0)
        *sigma))*lnmeanshift(sigma))
        binvalue[i] = binmidprice[i]*binprob[i]
    end
#
    trancheprice = sum(binvalue)
    return trancheprice
end
#
# oidv calculates implied daily and duration volatility for a call or a put
# using divide and conquer (the default for most models). Also see oidvnm.
# This uses an iterative process that uses otranche (above) to calculate the 
# sigma, here an implied sigma, from the existing option value (ovalue).
# The call variable is True for a call, False for a put. The convergence is 
# within the while loop. This function returns a tuple of two values, daily 
# IDV and duration IDV. 
#
function oidv(stock,strike,ovalue,days,call)
    epsilon = 1e-4
    low = 0.0
    high = 1.0
    daysigma = (high+low)/2
    dursigma = daysigma*durvol(days)
    tempop = otranche(stock,strike,dursigma,call)
    while tempop<=(ovalue-epsilon) || tempop>=(ovalue+epsilon)
        if tempop >= (ovalue+epsilon)
            high = daysigma
        else
            low = daysigma
        end
        daysigma = (high+low)/2
        dursigma = daysigma*durvol(days)
        tempop = otranche(stock,strike,dursigma,call)
    end
    # End of Loop!
    return [daysigma,dursigma]   
end
#
# oidvnm calculates implied daily and duration volatility for a call or a put
# using Newton's Method for convergence (default is divide and conquer).
# This uses an iterative process that uses otranche (above) to calculate the 
# sigma, here an implied sigma, from the existing option value (ovalue).
# The call variable is True for a call, False for a put. The convergence is 
# within the while loop. This function returns a tuple of two values, daily 
# IDV and duration IDV. 
#
function oidvnm(stock,strike,ovalue,days,call)
    seedsigma = 1e-6
    durseed = seedsigma*durvol(days)
    # NOTE: daysigma is supposed to be set at a reasonable estimate of the 
    # actual idv. The Newton method can explode if it is not (especially if you
    # enter option price, strike, and value data that are very unrealistic).
    # Consider setting daysigma at sqrt*time*ln(strike/stock). It was 
    # originally set at 0.05
    daysigma = (log(strike/stock))*sqrt(days)
    dursigma = daysigma*durvol(days)
    cutoff = 1e-4
    tempop = 0.00
    #
    # The loop starts here. You start with a test sigma and converge to the 
    # actual sigma. The convergence shown here (Newton's method) was designed 
    # by Alec Griffith '17 
    #
    while abs(tempop - ovalue) > cutoff
        tempop = otranche(stock,strike,dursigma,call)
        price2 = otranche(stock,strike,dursigma+durseed,call)
        deriv = (price2-tempop)/seedsigma
        daysigma -= (tempop-ovalue)/deriv
        dursigma = daysigma*durvol(days)
    end
    # End of Loop!
    return [daysigma,dursigma]
end
#
# Calculating the BSM put option price, traditional model. This requires the
# user to provide stock price, strike price, daily volatility, risk-free interest
# rate and days to expiry. (To calculate days use method daysto above).
# This returns the put price, the delta, and duration volatility as a tuple 
# array. See copo below for calls.
#
function popo(stock,strike,dayvol,days,rfir)
    d1 = log(stock/strike)+((rfir/365)+(dayvol^2)/2)*days
    durvol = dayvol*sqrt(days)
    delta = csnd(-d1/durvol)
    cumd2 = csnd(-(d1/durvol - durvol))
    discount = exp(-rfir*days/365)
    putpr = -(stock*delta)+(strike*discount*cumd2)
    return [putpr,delta,durvol]
end
#
# tdfecay adds an extension to the otranche calculator (Taboga model)   
# to calculate one-day time decay.
#
    
function tdecay(stock, strike, daysigma, oprice, days, call)
    days = days - 1.0
    dursigma = daysigma*durvol(days)
    oprice1d = otranche(stock,strike,dursigma,call)
    timedecay = oprice - oprice1d
    return timedecay
end