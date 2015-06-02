from flask import request

def send_slack_alert(coffee_level):
    if (coffee_level == 'low'):
        message = "Hey Datascope, the coffee beans are running low. Might be time to get some more."
        send_slack_notification(message)
    elif (coffee_level == 'out'):
        message = "Alert! We are out of coffee beans."
        send_slack_notification(message)


def send_slack_notification(message):
    payload = {
        "channel": "#check-yo-grind",
        "username": "Coffee Bean Alert",
        "text": message,
        "icon_emoji": ":coffee_bean_guy:"
        }
    print "Sending POST request: ", payload
    #response = requests.post("https://hooks.slack.com/services/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", data=payload)
