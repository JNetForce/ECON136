	# This is student program option_calc.py
# This is a modification of larger program delta_comp.py
# This program calculates a price array for put or call options
# at a range of strike prices from out of the money to
# in the money. This program requires a range of expiry prices
# (from 2 to 7). the current stock price, and daily volatility
# for the stock. Then inside the for loop the user must specify
# opo.popo for a put or opo.copo fpr a call. Both are modified 
# BSM, although you can use any option pricing model.
# Dedsigned by Prof Evans and students.
# This is version 1.1, March 24, 2018.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import op_util as opu
#
stosym = "AA"
call = True
days = (36, 22, 15, 8)
stopr = float(45.60)
dayvol = float(0.023434)
rfir = float (0.0225)
num_strike = len(days)
strike = np.linspace(40,52,13, dtype="float64")
size = len(strike)
#
# Set up the generic output matrix and initialize delta and price matrix.
#
out_su = np.arange(num_strike * size)
out_su = out_su.reshape((num_strike,size))
p_price = np.zeros_like(out_su, dtype="float64")
#
# Call in the BSM put model 
#
for i in range(0,num_strike):  # rows (all strikes, one expiry)
	for j in range(0,size):    # cols (each strike)
		if call:
			p_value, p_delta, p_durvol = opu.copo(stopr,strike[j],dayvol,days[i],rfir)
		else:
			p_value, p_delta, p_durvol = opu.popo(stopr,strike[j],dayvol,days[i],rfir)
		p_price[i,j] = p_value
#
# Plot the result (this will plot up to seven strikes .. to plot more put in a
# larger color palette. Below we have features common to both plots.
#
absis = np.array(strike, dtype="int")
sns.set_style("darkgrid")
cbcbgres7 = ['#edf8e9','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32']
cbcbgres7 = cbcbgres7[::-1]
cbcbreds7 = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']
cbcbreds7 = cbcbreds7[::-1]
cbcbblus7 = ['#eff3ff','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594']
cbcbblus7 = cbcbblus7[::-1]
cbcbgras7 = ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525']
cbcbgras7 = cbcbgras7[::-1]
#
# Plot the option values
#
sns.set_context("poster")
if call:
	sns.set_palette(cbcbreds7, 7)
else:
	sns.set_palette(cbcbgres7, 7)
fig, ax = plt.subplots()
fig.set_size_inches(14,10)
for m in range(0,num_strike):
    plt.plot(absis, p_price[m,...], label= days[m])
plt.axvline(x=stopr, color = "black")
if call:
	plt.title("Theoretical Call Option Values for Each Strike")
	plt.ylabel(" Call value")
else:
	plt.title("Theoretical Put Option Values for Each Strike")
	plt.ylabel(" Put value")
plt.xlabel("Strikes")
plt.legend()
plt.show() 
#
# END END END