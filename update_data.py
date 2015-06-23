import csv
import string
import os

import routes
import slack

web_root = os.path.dirname(os.path.abspath(__file__))

def process_request(value, year, month, day, hour, minute):
    coffee_level = get_coffee_level(value)
    handle_notifications(coffee_level)
    log_values = [str(coffee_level),str(value),str(year),str(month),str(day),str(hour),str(minute)]
    comma = ","
    new_log = comma.join(log_values)
    new_log += '\n'
    write_log(new_log)
    return


def handle_notifications(coffee_level):
    if(coffee_level == 'out' or coffee_level == 'low'):
        last_log = get_last_log()
        if(not(last_log['level'] == coffee_level)):
            if(slackIsOn()):
                slack.send_slack_alert(coffee_level)
            if(emailIsOn()):
                routes.send_email_alert(coffee_level)


def slackIsOn():
    settings = get_current_settings()
    print "SLACK IS: ", settings['slack']
    if(settings['slack'] == 'on'):
        return True
    else:
        return False


def emailIsOn():
    settings = get_current_settings()
    print "EMAIL IS: ", settings['email']
    if(settings['email'] == 'on'):
        return True
    else:
        return False


def get_coffee_level(value):
    value = int(value)
    bags_values = [2500,5000,7500,10000,70000]
    bags_levels = ['out','low','medium','high','full']
    plastic_values = [1500,3500,8000,13500,70000]
    plastic_levels = ['out','low','medium','high','full']

    # check settings to see container type
    with open(os.path.join(web_root, 'data','settings.csv'), 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            container = row['container']
    if container == 'bags':
        for i in range(0,len(bags_values)):
            if(value < bags_values[i]):
                return bags_levels[i]
    else:
        for i in range(0,len(plastic_values)):
            if(value < plastic_values[i]):
                return plastic_levels[i]
    return 'error'


def write_log(new_log):
    with open(os.path.join(web_root, 'data','updates.csv'), 'a') as csvfile:
        csvfile.write(new_log);


def get_last_log():
    with open(os.path.join(web_root, 'data','updates.csv'), 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            most_recent_log = {
            'level':row['level'],
            'value':row['value'],
            'year':row['year'],
            'month':row['month'],
            'day':row['day'],
            'hour':row['hour'],
            'minute':row['minute'],
            }
            if (len(most_recent_log['minute'])<2):
                most_recent_log['minute'] = '0' + row['minute']
    return most_recent_log

def get_all_logs():
    with open(os.path.join(web_root, 'data','updates.csv'), 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        count = 0
        all_logs = []
        for row in csvreader:
            count += 1
            all_logs.append({
            'level':row['level'],
            'value':row['value'],
            'year':row['year'],
            'month':row['month'],
            'day':row['day'],
            'hour':row['hour'],
            'minute':row['minute'],
            })
    return all_logs


def update_container(container_type):
    settings = get_current_settings()
    settings['container'] = container_type
    update_settings(settings)
    return settings

def update_email(email):
    settings = get_current_settings()
    settings['email'] = email
    update_settings(settings)
    return settings

def update_slack(slack):
    settings = get_current_settings()
    settings['slack'] = slack
    update_settings(settings)
    return settings


def get_current_settings():
    with open(os.path.join(web_root, 'data','settings.csv'), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            return row

def update_settings(new_settings):
    with open(os.path.join(web_root, 'data','settings.csv'), 'w') as csvfile:
        fieldnames = ['container','slack','email']
        csvwriter = csv.DictWriter(csvfile,fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerow(new_settings)

def add_email(email):
    emails = get_emails()
    if email not in emails:
        emails.append(email)
    update_emails(emails)
    return emails

def remove_email(email):
    emails = get_emails()
    emails.remove(email)
    update_emails(emails)
    return emails


def get_emails():
    with open(os.path.join(web_root, 'data','emails.csv'), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        emails = []
        for row in csvreader:
            emails.append(row['email'])
    return emails


def update_emails(emails):
    with open(os.path.join(web_root, 'data','emails.csv'), 'w') as csvfile:
        fieldnames = ['email']
        csvwriter = csv.DictWriter(csvfile,fieldnames=fieldnames)
        csvwriter.writeheader()
        for email in emails:
            csvwriter.writerow({'email': email})

if __name__ == '__main__':
    # enable reloading of the page if any files are changed
    settings = get_current_settings()
    settings['container'] = 'plastic'
    update_settings(settings)
