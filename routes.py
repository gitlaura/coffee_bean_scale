from flask import Flask
from flask import render_template
from flask import request
from flask_mail import Mail
from flask_mail import Message

import update_data

app =Flask(__name__)
mail=Mail(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'laura.rokita@gmail.com',
	MAIL_PASSWORD = 'Laura53087'
	)

mail=Mail(app)

def send_email_alert(coffee_level):
    subject = "Coffee Bean Alert"
    recipients = update_data.get_emails()
    if(coffee_level == 'low'):
        text = "Hey there, Datascope's coffee beans are running low. Might be time to get some more."
    elif(coffee_level == 'out'):
        text = "Alert! Datascope is out of coffee beans. Buy some more asap."
    for recipient in recipients:
        msg = Message("Coffee Bean Alert",sender='laura.rokita@gmail.com',recipients=[recipient])
        msg.body = text
        mail.send(msg)

@app.route('/')
def index():
    log = update_data.get_last_log()
    log = update_time(log)
    return render_template('index.html', log=log)

def update_time(log):
    if(int(log['hour']) < 13):
        log['post'] = "AM"
    else:
        log['post'] = "PM"
        log['hour'] = int(log['hour']) - 12
    return log

@app.route('/settings')
def settings():
    #update container
    container_type = request.args.get('container')
    email = request.args.get('email')
    slack = request.args.get('slack')
    email_to_remove = request.args.get('remove')
    email_to_add = request.args.get('add')
    if (container_type):
        settings = update_data.update_container(container_type)
    elif (email):
        settings = update_data.update_email(email)
    elif (slack):
        settings = update_data.update_slack(slack)
    else:
        settings = update_data.get_current_settings()

    if (email_to_remove):
        emails = update_data.remove_email(email_to_remove)
    elif (email_to_add):
        emails = update_data.add_email(email_to_add)
    else:
        emails = update_data.get_emails()

    return render_template('settings.html', settings=settings, emails=emails)


@app.route('/stats')
def stats():
    all_logs = update_data.get_all_logs()
    return render_template('stats.html', logs=all_logs)


@app.route('/update')
def update():
    value = request.args.get('value')
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    hour = request.args.get('hour')
    minute = request.args.get('minute')
    update_data.process_request(value, year, month, day, hour, minute)
    return render_template('update.html')


if __name__ == '__main__':
    # enable reloading of the page if any files are changed
    app.debug = True
    app.run()
