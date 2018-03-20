

# developed by

# Jeff McLaughlin, Krishna Kotha
# Catalyst Switching Technical Marketing

# Gabi Zapodeanu, TSA, Global Partner Organization


from cli import cli
import time
import difflib
import requests
import json
import urllib3

from code_init import SPARK_URL, SPARK_AUTH, SPARK_ROOM

from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def save_config():

    # save running configuration, use local time to create new config file name

    output = cli('show run')
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "/bootflash/" + timestr + "_shrun"

    f = open(filename,"w")
    f.write(output)
    f.close

    f = open('/bootflash/current_config_name','w')
    f.write(filename)
    f.close

    return filename


def compare_configs(cfg1, cfg2):

    # compare two config files

    d = difflib.unified_diff(cfg1, cfg2)

    diffstr = ""

    for line in d:
        if line.find('Current configuration') == -1:
            if line.find('Last configuration change') == -1:
                if (line.find("+++") == -1) and (line.find("---") == -1):
                    if (line.find("-!") == -1) and (line.find('+!') == -1):
                       if line.startswith('+'):
                            diffstr = diffstr + "\n" + line
                       elif line.startswith('-'):
                            diffstr = diffstr + "\n" + line

    return diffstr


def get_room_id(room_name):

    # find the Spark room id for the room with the name {room_name}

    payload = {'title': room_name}
    room_number = None
    url = SPARK_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    room_response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    room_list_json = room_response.json()
    room_list = room_list_json['items']
    for rooms in room_list:
        if rooms['title'] == room_name:
            room_number = rooms['id']
    return room_number


def post_room_message(room_id, message):

    # post message to the Spark room with the room id

    payload = {'roomId': room_id, 'text': message}
    url = SPARK_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


if __name__ == '__main__':

    syslog_input = cli("show logging | in %SYS-5-CONFIG_I")                                                     
    syslog_lines = syslog_input.split("\n")                     
    lines_no = len(syslog_lines)-2                                
    user_info = syslog_lines[lines_no]

    old_cfg_fn = "/bootflash/base-config"
    new_cfg_fn = save_config()

    f = open(old_cfg_fn)
    old_cfg = f.readlines()
    f.close

    f = open(new_cfg_fn)
    new_cfg = f.readlines()
    f.close

    diff =  compare_configs(old_cfg,new_cfg)
    print diff

    f = open("/bootflash/diff","w")
    f.write(diff)
    f.close

    device_name = cli("show run | in hostname")
    print device_name

    spark_room_id = get_room_id(SPARK_ROOM)

    post_room_message(spark_room_id, "The device with the " + device_name + " has these configuration changes:")
    post_room_message(spark_room_id, diff)
    post_room_message(spark_room_id, "   ")

    post_room_message(spark_room_id, user_info)

    print ("End Application Run")
