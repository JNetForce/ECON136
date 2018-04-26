# This is pop_main.py, designed to test op_util
# Located in \PyGo\PyTeach
# This is version 1.1 March 4, 2018
# Prof Gary Evans
# This would require a pth command unless it is in the
# same folder.
#
import op_util as opu
#
stosym = "AA"
days = int(11)
stopr = float(45.62)
strike = float(45.00)
dayvol = float(0.02343)
rfir = float (0.0225)
#
# Call the option calculator
# opu.copo returns a tuple array of call price, delta, and 
# duration volatility.
#
put_val = []
put_val = opu.popo(stopr,strike,dayvol,days,rfir)
#
print ("")
print ( stosym + " call: ")
print ( "Stock price: ", "%.3f" % stopr)
print ( "Strike price: ", "%.2f" % strike)
print ( "Historical daily volatility: ", "%.5f" % dayvol)
print ( "Duration volatility: ", "%.5f" % put_val[2])
print ( "Days to expiry: ", days)
print ( "The Delta:", "%.4f" % put_val[1])
print ( "Put option price: ", "%.4f" % put_val[0])
print ("")
