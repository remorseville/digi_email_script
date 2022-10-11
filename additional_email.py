import requests
import json
import pandas as pd


log = open("log.txt", "w")
data = pd.read_csv("data.csv")
order_list = data['order_number'].tolist()
email_list = data['email_address'].tolist()

api_key = "BRING YOUR OWN KEY"
headers = {
    'X-DC-DEVKEY': f'{api_key}',
    'Content-Type': "application/json"
}


def run_me(order_id, email_address):

    get_url = f'https://www.digicert.com/services/v2/order/certificate/{order_id}'
    get_response = requests.request("GET", get_url, headers=headers)
    get_data = get_response.text
    get_json_data = json.loads(get_data)
    email_array = []

    try:
        emails = get_json_data["additional_emails"]
    except KeyError:
        emails = "None"

    if emails is "None":
        email_array.append(email_address)
        final_array = email_array
    else:
        final_array = [email_address] + emails

    put_url = f'https://www.digicert.com/services/v2/order/certificate/{order_id}/additional-emails'
    payload = {
        "additional_emails": final_array
        }
    dump = json.dumps(payload)
    put_response = requests.request("PUT", put_url, data=dump, headers=headers)
    put_data = put_response.text
    log.write(str(order_id) + "\n" + "Old Array " + str(emails) + "\n" + "New Array " + str(final_array) + "\n" + "" + put_data)


def process():
    for i in range(len(order_list)):
        print(order_list[i], email_list[i])
        run_me(order_list[i], email_list[i])


process()

