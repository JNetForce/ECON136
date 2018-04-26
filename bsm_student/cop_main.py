# This is cop_main.py, designed to test op_util
# Located in \PyGo\PyTeach
# This is version 1.1 March 4, 2018
# Prof Gary Evans
# This would require a pth command unless it is in the
# same folder.
#
import op_util as opu
#
stosym = "TEST"
days = int(4)
stopr = float(100)
strike = float(102)
dayvol = float(0.03205)
rfir = float (0.0225)
#
# Call the option calculator
# opu.copo returns a tuple array of call price, delta, and 
# duration volatility.
#
call_val = []
call_val = opu.copo(stopr,strike,dayvol,days,rfir)
#
print ("")
print ( stosym + " call: ")
print ( "Stock price: ", "%.3f" % stopr)
print ( "Strike price: ", "%.2f" % strike)
print ( "Historical daily volatility: ", "%.5f" % dayvol)
print ( "Duration volatility: ", "%.5f" % call_val[2])
print ( "Days to expiry: ", days)
print ( "The Delta:", "%.4f" % call_val[1])
print ( "Call option price: ", "%.4f" % call_val[0])
print ("")
