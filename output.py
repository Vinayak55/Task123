import csv
import copy
from sector_timeperiod import SectorTimePeriod
from process_timeperiod import processTimePeriod
from datetime import date


RulesArray=[]

skipFirstRow=True

with open('budget.csv',newline='') as budget:
    reader=csv.reader(budget)
    for row in reader:
        if not skipFirstRow:  
            sector=row[3]
            period=row[2]
            amount=int(float(row[1]))
            #constructing object for each rule
            t=SectorTimePeriod()
            #copy 'sector' and 'period' respectively only if they exist with amount
            if period!='':
                t.setPeriod(period)
            if sector!='':
                t.setSector(sector)
            t.setAmount(amount)

            #append rules
            RulesArray.append(t)
            
        else:
            skipFirstRow=False


#Deep copy RulesArray to ImmutableRulesArray as some rules are going to change in RulesArray 
ImmutableRulesArray=copy.deepcopy(RulesArray)

#contains all rejected investment ID's
RejectedArray=[]

#same for Investments
skipFirstRow=True

with open('investments.csv',newline='') as invest:
    reader=csv.reader(invest)
    for row in reader:

        if not skipFirstRow:

            #extract sector, date, amount from each investment  
            sector=row[3]
            amount=int(float(row[2]))

            #expecting date to be in form of 'dd/mm/yy 
            dateArray=row[1].split('/')
            invest_date=date(day=int(dateArray[0]),month=int(dateArray[1]),year=int(dateArray[2]))

            #Each investment is assumed to be an oppurtunity (True)
            should_invest=True

            #traverse all rules for each investment
            for index in range(len(ImmutableRulesArray)):

                #extract sector, period, amount, start (date in the form of 'DateFormat' as we need to overwrite them)
                #from each rule.
                ruleSector=RulesArray[index].sector
                rulePeriod=RulesArray[index].period
                ruleAmount=RulesArray[index].amount
                ruleStart=RulesArray[index].start
                
                #if rule contains only 'sector'
                if rulePeriod is None and ruleSector is not None:

                    #only if sector matches and amount is greater than allocated for that sector
                    if ruleSector==sector and amount>ruleAmount:
                        RejectedArray.append(row[0])
                        should_invest=False
                        break

                #if rule contains only 'Time Period'
                elif rulePeriod is not None and ruleSector is None:
                    
                    TP=processTimePeriod(rulePeriod)
                    
                    if TP['period']=='Month' or TP['period']=='Quarter':
                        start=ruleStart.month
                        end=start+TP['add']

                        #..rule
                        if invest_date.month<=end and amount>ruleAmount:
                            RejectedArray.append(row[0])
                            should_invest=False
                            break
                        
                        #if investment date is outside of 'Month' and 'Quarter'
                        elif invest_date.month>end:

                            RulesArray[index].start.month=invest_date.month
                            RulesArray[index].amount=ImmutableRulesArray[index].amount

                    #period is 'Year'
                    else:
                        start=ruleStart.year
                        end=start+TP['add']

                        if invest_date.year<=end and amount>ruleAmount:
                            RejectedArray.append(row[0])
                            should_invest=False
                            break
                        
                        #investment date is outside of 'year'
                        elif invest_date.year>end:

                            #Replenish....
                            RulesArray[index].start.year=invest_date.year
                            RulesArray[index].amount=ImmutableRulesArray[index].amount
                
                #if rule contains both 'sector' and 'Time Period'
                else:

                    TP=processTimePeriod(rulePeriod)

                    if TP['period']=='Month' or TP['period']=='Quarter':
                        start=ruleStart.month
                        end=start+TP['add']
                        if invest_date.month<=end and (amount>ruleAmount and sector==ruleSector):
                            RejectedArray.append(row[0])
                            should_invest=False
                            break
                        elif invest_date.month>end:
                            RulesArray[index].start.month=invest_date.month
                            RulesArray[index].amount=ImmutableRulesArray[index].amount

                    else:
                        
                        start=ruleStart.year
                        end=start+TP['add']
                        if invest_date.year<=end and (amount>ruleAmount and sector==ruleSector):
                            RejectedArray.append(row[0])
                            should_invest=False
                            break

                        elif invest_date.year>end:
                            RulesArray[index].start.year=invest_date.year
                            RulesArray[index].amount=ImmutableRulesArray[index].amount

            # if investment passed all rules 
            if should_invest:
                for rule in RulesArray:

                    #if rule cotains only 'Time Period'
                    if rule.sector is None:
                        rule.amount=rule.amount-amount

                    #if rule contains only 'Sector'
                    elif rule.period is None:
                        if rule.sector==sector:
                            rule.amount=rule.amount-amount

                    #if rule contains both
                    else:
                        if rule.sector==sector:
                            rule.amount=rule.amount-amount
                
        else:
            skipFirstRow=False


#print rejected investment id
for i in RejectedArray:
    print(int(float(i)))