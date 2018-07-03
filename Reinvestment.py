from Miner import Miner
from Projection import Projection
from datetime import datetime
from datetime import timedelta
import numpy as np

class Reinvestment:
    __const1000GHS = 65
    __transferFees = 3.5
    __planDays = 90
    referralProjection = None

    def __init__(self, projection, days, minWait=1, minBuy=1, startDate=None, includeReferralBonus=False):
        if startDate is None:
            self.startDate = projection.startDate
        elif type(startDate) is str:
                self.startDate = datetime.strptime(startDate, '%m/%d/%Y')
        else:
            self.startDate = startDate
        
        self.days = days
        self.minWait = minWait
        self.minBuy = minBuy
        self.projection = projection
        self.includeReferralBonus = includeReferralBonus

        self.__project(self.projection)

        if self.includeReferralBonus:
            self.referralProjection = projection.clone(True)
            self.__project(self.referralProjection)

    
    
    def __project(self, projection):
        nextBuy = self.__getNextBuy(projection)
        while nextBuy.date < self.startDate + timedelta(self.days):
            projection.miners.append(Miner(
                hashRate=nextBuy.ghs, 
                startDate=nextBuy.date, 
                days=Reinvestment.__planDays, 
            ))

            projection.startDate = nextBuy.date
            projection.project()
            nextBuy = self.__getNextBuy(projection)


    def __getNextBuy(self, projection):
        revenue = np.array(projection.getAccRevenue())
        buyIndex = np.argmax(revenue > Reinvestment.__const1000GHS * self.minBuy)
        buyIndex = max(buyIndex, self.minWait)
        buyDate = projection.startDate + timedelta(days=buyIndex)
        buyUSD = revenue[buyIndex] - Reinvestment.__transferFees

        return NextBuy(buyDate, buyUSD)
        

class NextBuy:
    __const1000GHS = 65

    def __init__(self, date, usd):
        self.date = date
        self.usd = usd
        self.ghs = (usd/NextBuy.__const1000GHS) * 1000