import numpy as np

numofpolicies = 1000
pofchance = 0.1
numofsimulations = 1000000
years = 1

retentionlevel = 5000000
layer = 5000000

numofclaims = np.random.binomial(numofpolicies, pofchance, size=(years, numofsimulations))
totalnumofclaims = numofclaims.sum()
print(f"Total number of claims we will simulate: {totalnumofclaims}")

mean = 50000 #these are made up values 
standarddeviation = 20000 #these are made up values


sigma = np.sqrt(np.log(1+(standarddeviation**2)/ (standarddeviation**2)))
mu = np.log(mean) - (sigma**2) / 2
costperclaim = np.random.lognormal(mean=mu, sigma=sigma,size=totalnumofclaims)

netlossinsurer = np.zeros(numofsimulations)

endindex = np.cumsum(numofclaims.ravel())
startingindexs = np.hstack(([0], endindex[:-1]))
costpersim = np.add.reduceat(costperclaim, startingindexs)

reinsurerpayout = np.where((costpersim > retentionlevel) & (costpersim < retentionlevel +layer), costpersim - retentionlevel, 0)
reinsurerpayout = np.where(costpersim > retentionlevel + layer, layer, reinsurerpayout)
reinsurancepremium = np.mean(reinsurerpayout)

netlossinsurer = costpersim - reinsurerpayout


print(f"The annual premium for the reinsurance treaty should be: £{reinsurancepremium:,.2f}")

print("Aggregation complete.")
#print("Total loss for first 10 simulations:",netlossinsurer[:10])

expectedloss = np.mean(netlossinsurer)
var95 = np.percentile(netlossinsurer, 95)
var99 = np.percentile(netlossinsurer,99)
maxloss = np.max(netlossinsurer)


taillosses = netlossinsurer[netlossinsurer >= var99]
tvar99 = taillosses.mean()
print(f"Tail Value at Risk (TVaR 99%): £{tvar99:,.2f}")
worstlosses = np.sort(costpersim[-10:])
#print("Worst 10 net losses for the insurer:", worstlosses)

print(f"Expected Annual Loss: £{expectedloss:,.2f}")
print(f"Value at Risk (95%): £{var95:,.2f}")
print(f"Value at Risk (99%): £{var99:,.2f}")
print(f"Maximum Simulated Loss: £{maxloss:,.2f}")




#In my model I priced reinsurance as the expected payout, which is the actuarial pure premium. 
#But in reality premiums are also shaped by the reinsurance cycle soft markets push prices downand hard markets push them up  
#Plus loadings for risk appetite, expenses, and profit margins are not taken into account. So my premium estimate is lower than what reinsurers would actually charge.

#we use binomial because it is the industry standard, only 2 outcomes (claim occurs or does not), probability of each claim is ther same for each policy, claims are (mostly) independant.
#we use lognormal because it is also industry standard insurance claims are not normally distributed they are:
#skewed - most claims are small but few are extremely large.
#non negative - claims cost cannot be negative you cannot pay out -£10000
#heavytailed - there is a real non zero probability of a multimillion pound loss.

#Mean and std describe the average, assuming 100 claims happen each year with each claim exactly costing 50000 is a fantasy, the num of claims is random and the cost of the claim is also random the mean completely ignores this risk.
#Simulation reveals the risk it doesnt care about average it shows what actually happens in 10000 different versions of reality
#Answers questions that the mean and std fail to provide

#pricing - give you a better idea of what premium to charge to be profitable
#capital management - it tells you how much money to keep in reserves to avoid insolvency
#what is the worst case scenrio we must survive.
#how likely is a catastrophic year.

#improvements
#improvements could be made in the premium setting as we only include the expected value, and did not take into account others things such as risk appetite, hard or soft markets and other expenses.
#Also this model assumes total independance which isnt the case when there is a massive peril which causes claims to skyrocket as a natural disaster hitting a certain area.


