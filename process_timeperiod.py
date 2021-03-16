
def processTimePeriod(period):
    
    if period=='Month':
        return {'period':'Month','add':0}

    elif period=='Quarter':
        return {'period':'Quarter','add':2}

    else:
        return {'period':'Year','add':0}
