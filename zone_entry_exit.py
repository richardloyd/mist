import requests
import json
import datetime

def variable_names():
    mist_token = 'Enter Mist API Token'
    site_id = "Enter Site_ID"
    url = f"https://api.mist.com/api/v1/sites/{site_id}/vbeacons"

    payload = ""
    headers = {
        'Authorization': f'Token {mist_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()
    return data

def webhook_pull(beacon_data):
    # We will pushing the WebHook from the Mist Dashboard to Webhook.Site then sorting the data depending on 
    token_id = "Enter WebHook.Site API Token" 
    headers = {
        "api-key": "00000000-0000-0000-0000-000000000000"
    }

    url = f'https://webhook.site/token/{token_id}/requests?sorting=newest'
    r = requests.get(url, headers=headers)
    data = r.json()['data']
    dirty_list = []
    for item in data:
        uuid = item['uuid']
        # Assuming 'content' is a JSON string inside each 'item'
        if 'content' in item and item['content']:
            # Parse the JSON string in 'content'
            content_json = json.loads(item['content'])
            # Assuming 'events' is a list of events in content_json
            if 'events' in content_json:
                for event in content_json['events']:
                    if event['type'] == 'sdk':
                        for i in beacon_data:
                            # Accessing 'main' variables
                            event_id = event['id']
                            map_id = event['map_id']
                            name = event['name']
                            trigger = event['trigger']
                            #event['vbeacon_id'] =  i['name']
                            timestamp = datetime.datetime.fromtimestamp(event['timestamp'])
                            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            dirty_list.append({"timestamp":timestamp, "name":name, "event":event['vbeacon_id'], "trigger":trigger, "uuid":uuid, "identifer":event_id})
    return dirty_list

def parse_data(dirty_list):
    count = 0
    for i in dirty_list:
        for x in dirty_list:
            if i['uuid'] == x['uuid']:
                i['Completed'] = True
    return dirty_list

if __name__ == "__main__":
    beacon_data = variable_names()
    dirty_list = webhook_pull(beacon_data)
    final_list = parse_data(dirty_list)
    for i in final_list:
        if i['Completed'] == True and i['trigger'] == 'exit':
            continue
        print(i)


