"""
Name: plotter.py 
Authors: Oliver Giles & Max Potter
Date: July 2017
Description:
    - Use matplotlib to produce plots in order to analyse the performance of feorh.py
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#Get data
time,epoch,avFitness,avBreederFitness,wallDeathRate,killTotal = np.genfromtxt('fitnessAndDeath.txt', delimiter=',', skip_header=1, unpack=True)

#Clean data
time = time * 0.001
mask = np.where(avBreederFitness > 0)
avBreederFitness = avBreederFitness[mask]
timeReduced = time[mask]

#Model for residuals
polynomFit = lambda x,a,b: a*x+b #linear
# polynomFit = lambda x,a,b,c: a*x**2+b*x+c #2nd order poly
# polynomFit = lambda x,a,b,c,d: a*x**3+b*x**2+c*x+d #3rd order poly
fitParams, cov = curve_fit(polynomFit,time,killTotal)
resids = polynomFit(time,*fitParams) - killTotal

#Set up plot area
fig = plt.figure(figsize=(12,6))
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
frame1=fig.add_axes((.1,.3,.8,.6))
plt.title('Cumulative kills - state machine, normal movement')
plt.ylabel('kills')
plt.xlim([0,2000])
plt.plot(time,killTotal,'-b', label='Total kills') 
plt.plot(time,polynomFit(time,*fitParams),'-r', label='Linear best fit') #Best fit model
plt.legend()
frame1.set_xticklabels([]) #Remove x-tic labels for the first frame
#Residual plot
frame2=fig.add_axes((.1,.1,.8,.2))        
plt.plot(time,resids,'-r')
# frame2.set_yticks([0.0], minor=False)
# frame2.yaxis.grid(True, which='major')
plt.xlabel('time')
plt.xlim([0,2000])

#Plotting
# plt.plot(time,avFitness, label='Average over last 50 deaths')
# plt.plot(timeReduced,avBreederFitness, label='Gene pool average')
# plt.plot(time,wallDeathRate, label='% wall deaths')
# plt.plot(time,killTotal)
# plt.ylim(bottom = 0)
# plt.legend()

# plt.show()

plt.savefig('kills-sm-001aa.png')
