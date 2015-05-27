from flask import Flask
from flask import render_template
from flask import request

import update_data

app = Flask(__name__)


@app.route('/')
def index():
    log = update_data.get_last_log()
    return render_template('index.html', log=log)


@app.route('/settings')
def settings():
    return render_template('settings.html')


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
