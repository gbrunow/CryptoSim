from Investment import Investment
from Miner import Miner
from Projection import Projection
from Reinvestment import Reinvestment
from datetime import datetime

def printProjection(projection, referralProjection, totalInvested):
    days = (projection.endDate - datetime.now()).days        

    revenue = projection.getAccRevenue()[-1]
    refProfit = referralProjection.getAccRevenue()[-1]
    totalRevenue = revenue + refProfit

    profit = (refProfit+revenue) - totalInvested
    profitPercent = 100*profit/totalInvested

    print "{end} ({days:3} days)   ${revenue:.2f}    ${refProfit:.2f}       ${totalRevenue:.2f}     ${profit:.2f}       {profitPercent:.2f}%".format(
        end=projection.endDate, days=days, revenue=revenue, totalRevenue=totalRevenue, profit=profit, profitPercent=profitPercent, 
        refProfit=refProfit
    )

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
]

print "End Date                         Main        Referral       Total       Profit           %"
projection = Projection(startDate=miners[-1].startDate, miners=miners)
referralProjection = projection.clone(True)

printProjection(projection, referralProjection, totalInvested)

reinvestiment = Reinvestment(
    projection=projection, 
    days=15,
    minWait=1,
    minBuy=3.3,
    startDate=miners[-1].startDate, 
    includeReferralBonus=includeReferralBonus
)

printProjection(reinvestiment.projection, reinvestiment.referralProjection, totalInvested)

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


