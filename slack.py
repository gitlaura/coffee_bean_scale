import requests

def send_slack_alert(coffee_level):
    if (coffee_level == 'low'):
        payload = '{"channel":"#check-yo-grind", "username":"Coffee Bean Alert", "text":"The coffee beans are running low! Might be time to get some more.", "icon_emoji":":coffee_bean_guy:"}'
        send_slack_notification(payload)
    elif (coffee_level == 'out'):
        payload = '{"channel":"#check-yo-grind", "username":"Coffee Bean Alert", "text":"Alert! We are out of coffee beans.", "icon_emoji":":coffee_bean_guy:"}'
        send_slack_notification(payload)


def send_slack_notification(payload):
    print "Sending POST request: ", payload
    response = requests.post("https://hooks.slack.com/services/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", data=payload)
    print "RESPONSE: ", response.text
