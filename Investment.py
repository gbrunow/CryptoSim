from datetime import datetime
    
class Investment:

    def __init__(self, amount, date):
        self.amount = amount
        if type(date) is str:
            self.date = datetime.strptime(date, '%m/%d/%Y')
        else:
            self.date = date
        
