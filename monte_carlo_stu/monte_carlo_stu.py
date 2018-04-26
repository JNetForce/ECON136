# Incomplete student version
# HW9 Econ 136 Spring 2018
# Monte-Carlo simulator
#
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
#
# This below shows how to use numpy's random sampler that draws from a 
# standard normal distribution (mean 0, SD 1).
# Checking here to see if this numpy random sampler is any good.
sam_size = 252
rsample = np.zeros(sam_size)
for i in range(sam_size):
    rsample[i] = np.random.randn()  
center = np.mean(rsample, dtype=np.float64)
spread = np.std(rsample, dtype=np.float64)
print()
print("The mean should be close to zero, the spread close to one: ")
print ("Mean : ", center)
print ("Spread :", spread)
#
# Now build the simulator. Start with drift and volatility assumptions.
drift = 0.00356
sigma = 0.037874
start_price = 12.0
sims = 10
days = 252
span = 3
alpha = 2/(1+span)
days_after = [0 for i in range(span+1)]
days_after[0] = 4
days_after[3] = 1
for i in range(1,span):
    days_after[i] = days_after[i-1]*math.exp(-0.34657359*i)
print(days_after)


#
# The monte-carlo estimator
#
out_su = np.arange((sims+1)*days)
out_su = out_su.reshape((sims+1,days),order='C') # for col domination, order='F'
price = np.zeros_like(out_su, dtype="float64")
#
for i in range(0,sims + 1):
    price[i,0] = start_price
for j in range(1, days):
    price[-1, j] = price[-1, j-1]*math.exp(sigma*np.random.randn())
for i in range(0,sims):  # rows (each a different simulation)
    poisson_counter = span
    for j in range(1,days):    # cols (each a new day!)
        # And below is where you replace the placeholder with the Monte Carlo equation. 
        if poisson_counter > 0:
            price[i,j] = price[i,j-1]*math.exp(drift + days_after[3-poisson_counter]*sigma*np.random.randn())
            poisson_counter-= 1
        elif (np.random.poisson(lam = (30/252)) > 1):
            poisson_counter = 3
            price[i,j] = price[i,j-1]*math.exp(drift + days_after[3 - poisson_counter]*sigma*np.random.randn())
        else:
            price[i,j] = price[i,j-1]*math.exp(drift + sigma*np.random.randn())

sns.set_style("darkgrid")
cbcbgres7 = ['#edf8e9','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32']
cbcbgres7 = cbcbgres7[::-1]
cbcbreds7 = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']
cbcbreds7 = cbcbreds7[::-1]
cbcbblus7 = ['#eff3ff','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594']
cbcbblus7 = cbcbblus7[::-1]
cbcbgras7 = ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525']
cbcbgras7 = cbcbgras7[::-1]


for i in range(0, sims):
    if i == sims-1:
        plt.plot(price[i,], label = "Drift Only")
    else:
        plt.plot(price[i,], label = "Drift+Sigma " + str(i))

# df = pd.DataFrame({'B': [4, 2, 1]})
# print(pd.ewma(df, com = 1))
plt.ylabel("Prices")
plt.xlabel("Days")
plt.legend()
# plt.show()
#
print("Done")
# Plot the result.
