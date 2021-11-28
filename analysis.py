# -*- coding: utf-8 -*-
import pprint
import json
import time
from datetime import datetime


pp = pprint.PrettyPrinter(indent=4)


def findStepsInRange(start, end, file):
    
    pass

def findStepsByMonth():
    # load the steps file
    file = 'exports/dataset-1638116329.json'
    with open(file) as f:
        data = json.load(f)

    # search the file for each month
    for i in range(12):
        month = i+1
        if month < 12:
            # set the start of the month for the current year
            start_of_month = datetime.now().date().replace(month=month, day=1) 
            next_month = datetime.now().date().replace(month=month+1, day=1) 
            month_name = start_of_month.strftime("%B")
            # convert date ns timestamp
            start_timestamp = datetime(
                start_of_month.year,
                start_of_month.month,
                start_of_month.day, 0, 0).timestamp()* 1000000000
            next_timestamp = datetime(
                next_month.year,
                next_month.month,
                next_month.day, 0, 0).timestamp()* 1000000000
            
            # find the sum of steps in that month
            steps = sum(d['value'][0]['intVal'] for d in data['point'] if start_timestamp < int(d['startTimeNanos']) < next_timestamp)

            print( month_name, steps)
            print(f"average per day: {int(steps/30)}")
        elif month == 12:
            # just find the rest
            start_of_month = datetime.now().date().replace(month=month, day=1) 
            month_name = start_of_month.strftime("%B")

            start_timestamp = datetime(
                start_of_month.year,
                start_of_month.month,
                start_of_month.day, 0, 0).timestamp()* 1000000000
            steps = sum(d['value'][0]['intVal'] for d in data['point'] if start_timestamp < int(d['startTimeNanos']))
            print( month_name, steps)
            print(f"average per day: {int(steps/30)}")

def main():
    pass

def test():
    file = 'exports/dataset-1638111837.json'
    with open(file) as f:
        data = json.load(f)

    start_of_month = datetime.now().date().replace(month=1, day=1) 
    next_month = datetime.now().date().replace(month=2, day=1) 
    # ns timestamp
    start_timestamp = int(datetime(
        start_of_month.year,
        start_of_month.month,
        start_of_month.day, 0, 0).timestamp()* 1000000000)
    next_timestamp = int(datetime(
        next_month.year,
        next_month.month,
        next_month.day, 0, 0).timestamp()* 1000000000)
    # if start_timestamp < d['startTimeNanos'] < next_timestamp:
    #     pass
    steps = sum(d['value'][0]['intVal'] for d in data['point'] if start_timestamp < int(d['startTimeNanos']) < next_timestamp)
    print(next_month.strftime("%B"))
    print(steps)

if __name__ == '__main__':
    findStepsByMonth()
