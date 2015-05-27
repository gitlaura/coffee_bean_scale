import csv
import string
import os

web_root = os.path.dirname(os.path.abspath(__file__))

def process_request(value, year, month, day, hour, minute):
    log_values = [str(value),str(year),str(month),str(day),str(hour),str(minute)]
    comma = ","
    new_log = comma.join(log_values)
    new_log += '\n'
    write_log(new_log)
    return

def process_request_two(value, year, month, day, hour, minute):
    log_values = [str(value)]
    comma = ","
    new_log = comma.join(log_values)
    new_log += '\n'
    write_log(new_log)
    return

def write_log(new_log):
    with open(os.path.join(web_root, 'data','updates.csv'), 'a') as csvfile:
        csvfile.write(new_log);

def get_last_log():
    with open(os.path.join(web_root, 'data','updates.csv'), 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            most_recent_log = {
            'value':row['value'],
            'year':row['year'],
            'month':row['month'],
            'day':row['day'],
            'hour':row['hour'],
            'minute':row['minute'],
            }
            if (len(most_recent_log['minute'])<2):
                most_recent_log['minute'] = '0' + row['minute']
            print most_recent_log
    return most_recent_log

def get_all_logs():
    with open(os.path.join(web_root, 'data','updates.csv'), 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        count = 0
        all_logs = []
        for row in csvreader:
            count += 1
            all_logs.append({
            'value':row['value'],
            'year':row['year'],
            'month':row['month'],
            'day':row['day'],
            'hour':row['hour'],
            'minute':row['minute'],
            })
    return all_logs
