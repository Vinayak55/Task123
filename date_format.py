
class DateFormat:
    def __init__(self,day=1,month=1,year=2020):
        self.day=day
        self.month=month
        self.year=year

    def __str__(self):
        return str(self.day)+'/'+str(self.month)+'/'+str(self.year)