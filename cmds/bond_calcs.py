import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.optimize import root

def price_bond(ytm, T, cpn, cpnfreq=2, face=100, accr_frac=None):
    ytm_n = ytm/cpnfreq
    cpn_n = cpn/cpnfreq
    
    if accr_frac is None:
        accr_frac = 0

    if cpn==0:
        accr_frac = 0
        
    N = T * cpnfreq
    price = face * ((cpn_n / ytm_n) * (1-(1+ytm_n)**(-N)) + (1+ytm_n)**(-N)) * (1+ytm_n)**(accr_frac)
    return price




def ytm(price, T, cpn, cpnfreq=2, face=100, accr_frac=None,solver='fsolve',x0=.01):
    
    pv_wrapper = lambda y: price - price_bond(y, T, cpn, cpnfreq=cpnfreq, face=face, accr_frac=accr_frac)

    if solver == 'fsolve':
        ytm = fsolve(pv_wrapper,x0)
    elif solver == 'root':
        ytm = root(pv_wrapper,x0)
    return ytm





def crsp_data_calculate_ytm(data, colkey='price', append=False):

    calcs = pd.DataFrame(index=data.index,columns=['ytm'])
    for i in calcs.index:        
        calcs.loc[i,'ytm'] = ytm(data.loc[i,colkey], data.loc[i,'ttm'], data.loc[i,'cpn rate']/100)

    calcs['ytm'] = calcs['ytm'].astype(float)

    return calcs







