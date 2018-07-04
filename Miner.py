from datetime import datetime
from datetime import timedelta
from copy import deepcopy
    
class Miner:
    __dailyGhsRevenue = 0.9/1000 # $0.9 per 1000GHS per day

    dailyRevenue = 0
    expectedRevenue = 0


    def __init__(self, hashRate, startDate, endDate=None, days=None):

        if type(startDate) is str:
            self.startDate = datetime.strptime(startDate, '%m/%d/%Y')
        else:
            self.startDate = startDate
        
        if endDate is None:
            self.endDate = self.startDate + timedelta(days=days)
        elif type(endDate) is str:
            self.endDate = datetime.strptime(endDate, '%m/%d/%Y')
        else:
            self.endDate = endDate
        
        self.hashRate = hashRate
        self.days = (self.endDate - self.startDate).days
        self.dailyRevenue = Miner.__dailyGhsRevenue * self.hashRate
        self.expectedRevenue = self.days * self.dailyRevenue

    def clone(self, isReferral=False):
        hash = self.hashRate
        if isReferral:
            hash = hash * 0.15
        return Miner(hash, self.startDate, self.endDate, self.days)
    
    def getRevenue(self, date):
        if type(date) is str:
            date = datetime.strptime(date, '%m/%d/%Y')

        revenue = 0
        if date > self.startDate and date <= self.endDate:
            revenue = self.dailyRevenue
        
        return revenue
    
    def getRevenueFrom(self, start, end):
        if type(start) is str:
            start = datetime.strptime(start, '%m/%d/%Y')
        if type(end) is str:
            end = datetime.strptime(end, '%m/%d/%Y')

        accRevenue = 0
        start = max(self.startDate, start)
        end = min(self.endDate, end)
        if start <= end:
            days = (end - start).days
            accRevenue = days * self.dailyRevenue

        return accRevenue

    def getAccRevenue(self, start, end):
        if type(start) is str:
                start = datetime.strptime(start, '%m/%d/%Y')
        if type(end) is str:
            end = datetime.strptime(end, '%m/%d/%Y')

        accRevenue = []

        days = (end - start).days
        for day in range(days):
            end = start + timedelta(days=day)
            accRevenue.append(self.getRevenueFrom(start, end))

        return accRevenue
        

