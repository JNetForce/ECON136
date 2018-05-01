# HW9 Econ 136 Spring 2018
# Monte-Carlo simulator
# /Applications/Julia-0.6.app/Contents/Resources/julia/bin/julia ~/Documents/projects/ECON136/monte_carlo_stu/monte_carlo_stu.jl

using PyPlot
using Distributions

# This below shows how to use numpy's random sampler that draws from a
# standard normal distribution (mean 0, SD 1).
# Checking here to see if this numpy random sampler is any good.
sam_size = 252
rsample = zeros(sam_size)

for i in range(1, sam_size)
    rsample[i] = randn()
end

center = mean(rsample)
spread = std(rsample)

println("The mean should be close to zero, the spread close to one: ")
println("Mean : ", center)
println("Spread :", spread)

# Now build the simulator. Start with drift and volatility assumptions.
drift = 0.00356
sigma = 0.037874
start_price = 12.0
sims = 10
days = 252
span = 3
alpha = 2/(1+span)
days_after = [0.0 for i in 0:span+1]
days_after[1] = 4.0
days_after[4] = 1.0
for i in range(2, span)
    days_after[i] = days_after[i-1]*exp(-0.34657359*i)
end
# println(days_after)

# The monte-carlo estimator
out_su = range(0, (sims+1)*days)
out_su = reshape(out_su, (sims+1,days)) # for col domination, order='F' ?C
price = zeros(Float64, size(out_su))
#
for i in range(1, sims+1)
    price[i,1] = start_price
end
# println(price)

for j in range(2, days-1)
    price[1,j] = price[1, j-1]*exp(sigma*randn()) # ??????
end

for i in range(1, sims+1)  # rows (each a different simulation)
    poisson_counter = span
    for j in range(2, days-1)    # cols (each a new day!)
        # And below is where you replace the placeholder with the Monte Carlo equation.
        if poisson_counter > 0
            price[i,j] = price[i,j-1]*exp(drift + days_after[3-poisson_counter+1]*sigma*randn())
            poisson_counter-= 1
        elseif pdf(Poisson(30/252), 1) > 1
            poisson_counter = 3
            price[i,j] = price[i,j-1]*exp(drift + days_after[3-poisson_counter+1]*sigma*randn())
        else
            price[i,j] = price[i,j-1]*exp(drift + sigma*randn())
        end
    end
end
# sns.set_style("darkgrid")
# cbcbgres = ['#edf8e9','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45','#005a32']
# cbcbgres = cbcbgres[::-1]
# cbcbreds = ['#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d']
# cbcbreds = cbcbreds[::-1]
# cbcbblus = ['#eff3ff','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#084594']
# cbcbblus = cbcbblus[::-1]
# cbcbgras = ['#f7f7f7','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525']
# cbcbgras = [::-1]

fig = figure("lineplot", figsize=(10,10))
for i in range(1, sims+1)
    if i == sims-1
        plot(price[i,:], label = "Drift Only")
    else
        plot(price[i,:], label = "Drift+Sigma " * string(i))
    end
end

# println(price)

# df = pd.DataFrame({'B': [4, 2, 1]})
# print(pd.ewma(df, com = 1))
ylabel("Prices")
xlabel("Days")
legend()
show()
#
println("Done")
# Plot the result.
