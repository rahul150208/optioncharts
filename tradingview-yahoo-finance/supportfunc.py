
from datetime  import timedelta

import datetime as dt


def check_holidays(date):
    if(date==dt.datetime(2024,4,17)):
        return dt.datetime(2024,4,16)
    elif(date==dt.datetime(2024,5,1)):
        return dt.datetime(2024,4,30)
    elif(date==dt.datetime(2024,7,17)):
        return dt.datetime(2024,7,16)
    elif(date==dt.datetime(2024,4,11)):
        return dt.datetime(2024,4,10)
    elif(date==dt.datetime(2024,8,15)):
        return dt.datetime(2024,8,14)
    else:
        return date
    
def expiryofmonth(year, month, day):
    
    input_date = dt.datetime(year, month, day)
    
    
        
    if (input_date > dt.datetime(2023,9,1)):
        days_ahead = (3 - input_date.weekday() + 7) % 7   # FOR WED EXPIRY OF BANKNIFTY CHANGE 3-->2
    else:
        days_ahead = (3 - input_date.weekday() + 7) % 7  # before sep 2023 expiry of banknifty used to be thursday
        
    if days_ahead == 0:  # If the date is already a Wednesday
        days_ahead = 0
    next_wednesday = input_date + timedelta(days=days_ahead)
    
    # Find the last day of the month
    if month == 12:
        last_day_of_month = dt.datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day_of_month = dt.datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Check if next Wednesday is the last Wednesday of the month
    last_wednesday = last_day_of_month - timedelta(days=(last_day_of_month.weekday() - 3) % 7)   # make it back to 2 for banknifty wednesday expiry
    # print(next_wednesday , last_wednesday)
    if  ( (next_wednesday >= last_wednesday) and ( input_date < dt.datetime(2024,3,1)) ):
        # Find the last Thursday of the month
        
        last_thursday = last_wednesday + timedelta(days=1)
        if(last_thursday == dt.datetime(2024,7,17) ):
            
            return check_holidays(last_thursday)
        else:
            return check_holidays(last_thursday)
    else:
        if(next_wednesday == dt.datetime(2024,7,17) ):
            return check_holidays(next_wednesday)
        else:
            return check_holidays(next_wednesday)

