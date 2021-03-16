from date_format import DateFormat

class SectorTimePeriod:
    def __init__(self):
        self.period=None
        self.amount=0
        self.sector=None
        self.start=DateFormat()

    def __str__(self):
        if self.period is None:
            return self.sector+" "+str(self.amount)
        elif self.sector is None:
            return self.period+" "+str(self.amount)
        else:
            return self.sector+" "+self.period+" "+str(self.amount)
        

    def setStart(self,start):
        self.start=start
    
    
    def setPeriod(self,period):
        self.period=period


    def setSector(self,sector):
        self.sector=sector


    def setAmount(self,amount):
        self.amount=amount