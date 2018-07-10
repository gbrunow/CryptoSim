import numpy as np
import pickle
from Investment import Investment
from Miner import Miner
from Projection import Projection
from Reinvestment import Reinvestment
from datetime import datetime

def printProjection(projection, referralProjection, totalInvested, minimumBuy="No buy"):
    days = (projection.endDate - datetime.now()).days        

    revenue = projection.getAccRevenue()[-1]
    refProfit = referralProjection.getAccRevenue()[-1]
    totalRevenue = revenue + refProfit

    profit = (refProfit+revenue) - totalInvested
    profitPercent = 100*profit/totalInvested

    print "{end} ({days:3} days)   ${revenue:.2f}    ${refProfit:.2f}       ${totalRevenue:.2f}     ${profit:.2f}       {profitPercent:.2f}%        {minimumBuy}".format(
        end=projection.endDate, days=days, revenue=revenue, totalRevenue=totalRevenue, profit=profit, profitPercent=profitPercent, 
        refProfit=refProfit, minimumBuy=minimumBuy
    ),

    # for miner in projection.miners:
    #     print "{hash}GHS    ${revenue:.2f}/day   {start} - {end}".format(
    #         hash=int(miner.hashRate), revenue=miner.dailyRevenue, start=miner.startDate, end=miner.endDate
    #     )

printTitle = True
includeReferralBonus = True

investments = [
    Investment(1800, '5/30/2018'),
    Investment(300, '5/30/2018'),
    Investment(300, '5/30/2018'),
    Investment(10, '6/4/2018'),
    Investment(10, '6/8/2018')
]

totalInvested = 0
for investiment in investments:
    totalInvested = totalInvested + investiment.amount

miners = [
    Miner(hashRate=40600, startDate='5/31/2018', days=90),
    Miner(hashRate=3450, startDate='6/4/2018', days=90),
    Miner(hashRate=1000, startDate='6/5/2018', days=90),
    Miner(hashRate=1270, startDate='6/7/2018', days=90),
    Miner(hashRate=1900, startDate='6/9/2018', days=90),
    Miner(hashRate=1540, startDate='6/11/2018', days=90),
    Miner(hashRate=1300, startDate='6/13/2018', days=90),
    Miner(hashRate=1070, startDate='6/14/2018', days=90),
    Miner(hashRate=3000, startDate='6/17/2018', days=90),
    Miner(hashRate=4800, startDate='6/27/2018', days=90),
    Miner(hashRate=6500, startDate='7/3/2018', days=90),
    Miner(hashRate=3700, startDate='7/7/2018', days=90),
    Miner(hashRate=11950, startDate='7/9/2018', days=90)
]

print "End Date                         Main        Referral       Total       Profit           %       Min Buy (GHS)"
projection = Projection(startDate=miners[-1].startDate, miners=miners)
referralProjection = projection.clone(True)

printProjection(projection, referralProjection, totalInvested)

bestProfit = 0
best = None
for i in range(10):
    print "\n============= week " + str(i) + " =============" 
    for minGHS in np.arange(1, 7.5, 0.05):
        clone = projection.clone()
        reinvestiment = Reinvestment(
            projection=clone, 
            days=7*(i+1),
            minWait=0,
            minBuy=minGHS,
            startDate=miners[-1].startDate, 
            includeReferralBonus=includeReferralBonus
        )

        revenue = clone.getAccRevenue()[-1]
        refProfit = clone.clone(True).getAccRevenue()[-1]
        totalRevenue = revenue + refProfit

        profit = (refProfit+revenue) - totalInvested
        profitPercent = 100*profit/totalInvested

        if profitPercent >= bestProfit:
            if profitPercent > bestProfit:
                print ""
                printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested, minGHS)
                best = clone
            else:
                print str(minGHS),
            bestProfit = profitPercent
    projection = best


# reinvestiment = Reinvestment(
#     projection=projection, 
#     days=90,
#     minWait=1,
#     minBuy=1,
#     startDate=miners[-1].startDate, 
#     includeReferralBonus=includeReferralBonus
# )

# printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested)

# reinvestiment = Reinvestment(
#     projection=projection, 
#     days=42,
#     minWait=4,
#     startDate=miners[-1].startDate, 
#     includeReferralBonus=includeReferralBonus
# )

# printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested)

# reinvestiment = Reinvestment(
#     projection=projection, 
#     days=40,
#     minWait=4,
#     startDate=miners[-1].startDate, 
#     includeReferralBonus=includeReferralBonus
# )
# printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested)

# reinvestiment = Reinvestment(
#     projection=projection, 
#     days=90,
#     minWait=4,
#     startDate=miners[-1].startDate, 
#     includeReferralBonus=includeReferralBonus
# )
# printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested)

# profitMiners = reinvestiment.projection.miners
# profitMiners.append(reinvestiment.referralProjection.miners)


