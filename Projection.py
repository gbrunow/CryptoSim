from Miner import Miner
from datetime import datetime
from datetime import timedelta
import numpy as np

class Projection:
    miners = None
    startDate = None
    endDate = None
    days = None
    minerProjections = None
    projections = None
    revenue = None
    
    def __init__(self, startDate=None, days=None, miners = []):
        if startDate is not None:
            if type(startDate) is str:
                self.startDate = datetime.strptime(startDate, '%m/%d/%Y')
            else:
                self.startDate = startDate
            
            if days is not None:
                self.endDate = self.startDate + timedelta(days=days)
                self.days = (self.endDate - self.startDate).days

        self.miners = miners
        if len(miners) > 0:
            self.project()
    
    def clone(self, isReferral=False):
        projection = Projection(self.startDate, self.days)
        for miner in self.miners:
            projection.miners.append(miner.clone(isReferral))
            projection.project()

        return projection

    def project(self):
        self.minerProjections = []
        self.projections = []
        if self.startDate is None:
            self.startDate = self.miners[0].startDate
            for miner in self.miners:
                self.startDate = min(self.startDate, miner.startDate)
                
        self.endDate = self.miners[0].endDate
        for miner in self.miners:
            self.endDate = max(self.endDate, miner.endDate)
        
        for miner in self.miners:
            self.minerProjections.append(miner.getAccRevenue(self.startDate, self.endDate))
        
        self.projections = np.sum(self.minerProjections, axis=0)
        self.revenue = self.projections[-1]

    def getAccRevenue(self, start=None, end=None):
        if start is None:
            start = self.startDate
        elif type(start) is str:
                start = datetime.strptime(start, '%m/%d/%Y')

        if end is None:
            end = self.endDate                
        if type(end) is str:
            end = datetime.strptime(end, '%m/%d/%Y')

        revenue = 0

        if start <= self.endDate:
            start = (max(start, self.startDate) - self.startDate).days
            size = (min(end, self.endDate) - self.startDate).days
            revenue = self.projections[start:size]


        return revenue

        
