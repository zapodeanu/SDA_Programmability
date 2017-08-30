# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

# !/usr/bin/env python3

import requests
import json

import requests.packages.urllib3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from sda_init import GOOGLE_API_KEY

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# use the DNA Center controller

DNAC_URL = 'https://172.28.97.211/api/v1'
DNAC_USER = 'admin'
DNAC_PASS = 'Cisco123'


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_service_ticket(username, password):
    """
    Create the authorization ticket required to access APIC-EM
    Call to APIC-EM - /ticket
    :param username: the username
    :param password: the password
    :return: ticket
    """

    payload = {'username': username, 'password': password}
    url = DNAC_URL + '/ticket'
    header = {'content-type': 'application/json'}
    ticket_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    if not ticket_response:
        print('No data returned!')
    else:
        ticket_json = ticket_response.json()
        ticket = ticket_json['response']['serviceTicket']
        return ticket


def create_area(area_name, ticket):
    """
    The function will create a new area with the name {area_name}
    :param area_name: DNA C area name
    :param ticket: DNA C ticket
    :return: none
    """
    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "type": "area"
                }
            }
        ],
        "groupNameHierarchy": "Global/USA/" + area_name,
        "groupTypeList": [
            "SITE"
        ],
        "systemGroup": False,
        "parentId": "7a8e6ed5-db65-401b-8cf6-6382864b0508",
        "name": area_name,
        "id": ""
    }
    url = DNAC_URL + '/group'
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def create_site(site_name, area_name, address, ticket):
    """
    The function will create a new site with the name {site_name}, part of the area with the name {area_name}
    :param site_name: DNA C site name
    :param area_name: DNA C area name
    :param address: site address
    :param ticket: DNA C ticket
    :return: none
    """
    # get the area id for the area name

    area_id = get_area_id(area_name, ticket)

    # get the geolocation info for address

    geo_info = get_geo_info(address, GOOGLE_API_KEY)
    print('\nGeolocation info for the address ', address, ' is:')
    pprint(geo_info)

    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "country": "United States",
                    "address": address,
                    "latitude": geo_info['lat'],
                    "type": "building",
                    "longitude": geo_info['lng']
                }
            }
        ],
        "groupNameHierarchy": "Global/USA/" + site_name,
        "groupTypeList": [
            "SITE"
        ],
        "systemGroup": False,
        "parentId": area_id,
        "name": site_name,
        "id": ""
    }
    url = DNAC_URL + '/group'
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def create_floor(site_name, floor_name, floor_number, ticket):
    """
    The function will  create a floor in the building with the name {site_name}
    :param site_name: DNA C site name
    :param floor_name: floor name
    :param floor_number: floor number
    :param ticket: DNA C ticket
    :return: none
    """
    # get the site id
    site_id = get_site_id(site_name, ticket)

    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "type": "floor"
                }
            },
            {
                "nameSpace": "mapGeometry",
                "attributes": {
                    "offsetX": "0.0",
                    "offsetY": "0.0",
                    "width": "300.0",
                    "length": "100.0",
                    "geometryType": "DUMMYTYPE",
                    "height": "20.0"
                }
            },
            {
                "nameSpace": "mapsSummary",
                "attributes": {
                    "floorIndex": floor_number
                }
            }
        ],
        "groupNameHierarchy": "Global/USA/Lake Oswego/" + floor_name,
        "groupTypeList": [
            "SITE"
        ],
        "name": floor_name,
        "parentId": site_id,
        "systemGroup": False,
        "id": ""
    }
    url = DNAC_URL + '/group'
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def get_device_id(device_sn, ticket):
    """
    The function will return the DNA C device id for the device with serial number {device_sn}
    :param device_sn:
    :param ticket: DNA C ticket
    :return: DNA C device id
    """
    url = DNAC_URL + '/network-device/serial-number/' + device_sn
    header = {'content-type': 'application/json', 'X-Auth-Token': ticket}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    device_id = device_info['response']['id']
    return device_id


def assign_device_site(device_sn, site_name, ticket):
    """

    :param device_sn:
    :param site_name: DNA C site name
    :param ticket: DNA C ticket
    :return:
    """
    site_id = get_site_id(site_name, ticket)
    device_id = get_device_id(device_sn, ticket)
    url = DNAC_URL + '/group/' + site_id + '/member'
    payload = {"networkdevice":[device_id]}
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    print('\nDevice with the SN: ', device_sn, 'assigned to site: ', site_name)



def get_area_id(area_name, ticket):
    """
    The function will return the DNA C area id for the area with the name {area_name}
    :param area_name: DNA C area name
    :param ticket: DNA C ticket
    :return: DNA C area id
    """
    url = DNAC_URL + '/group?groupType=SITE'
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    area_response = requests.get(url, headers=header, verify=False)
    area_json = area_response.json()
    area_list = area_json['response']
    for area in area_list:
        if area_name == area['name']:
            area_id = area['id']
    return area_id


def get_site_id(site_name, ticket):
    """
    The function will get the DNA C site id for the site with the name {site_name}
    :param site_name: DNA C site name
    :param ticket: DNA C ticket
    :return: DNA C site id
    """
    url = DNAC_URL + '/group?groupType=SITE'
    header = {'content-type': 'application/json','X-Auth-Token': ticket}
    site_response = requests.get(url, headers=header, verify=False)
    site_json = site_response.json()
    site_list = site_json['response']
    for site in site_list:
        if site_name == site['name']:
            site_id = site['id']
    return site_id


def get_geo_info(address, google_key):
    """
    The function will access Google Geolocation API to find the longitude/latitude for a address
    :param address: address, including ZIP and Country
    :param google_key: Google API Key
    :return: longitude/latitude
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+google_key
    header = {'content-type': 'application/json'}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    location_info = response_json['results'][0]['geometry']['location']
    return location_info


def main():
    """

    """

    # create a DNA C ticket

    dnac_ticket = get_service_ticket(DNAC_USER, DNAC_PASS)
    print('\nDNA Center ticket: ', dnac_ticket)

    # create the DNA C areas

    area_us = 'USA'
    create_area(area_us, dnac_ticket)

    area_eur = 'EUROPE'
    create_area(area_eur, dnac_ticket)

    # get the DNA C area ids

    area_us_id = get_area_id(area_us, dnac_ticket)
    print('\nDNA C Area Id for USA is: ', area_us_id)

    area_eur_id = get_area_id(area_eur, dnac_ticket)
    print('\nDNA C Area Id for EUROPE is: ', area_eur_id)

    # create the DNA C sites

    site_usa_or = 'Lake Oswego'
    site_add_usa_or = '5400 SW Meadows Rd, Lake Oswego, Oregon 97035, United States'
    create_site(site_usa_or, area_us, site_add_usa_or, dnac_ticket)

    site_usa_ca = 'San Jose'
    site_add_usa_ca = '725 Alder Dr, Milpitas, CA 95035, United States'
    create_site(site_usa_ca, area_us, site_add_usa_ca, dnac_ticket)

    site_eur_ned = 'Amsterdam'
    site_add_eur_ned = 'Haarlerbergweg 15, 1101 CH Amsterdam-Zuidoost, Netherlands'
    create_site(site_eur_ned, area_eur, site_add_eur_ned, dnac_ticket)

    # create a new DNA C floor

    floor_usa_or = 'Floor 3'
    floor_number = 3
    create_floor(site_usa_or, floor_usa_or, floor_number, dnac_ticket)

    # assign devices to sites

    sn_3650 = 'FDO1915E0EG'
    sn_9300 = 'FCW2123L0N3'
    sn_2960 = 'FOC1537W1ZY'
    sn_2900_1 = 'FTX1840ALC1'
    sn_2900_2 = 'FTX1840ALBY'

    assign_device_site(sn_9300, site_usa_or, dnac_ticket)
    assign_device_site(sn_3650, site_usa_or, dnac_ticket)
    assign_device_site(sn_2960, site_usa_ca, dnac_ticket)
    assign_device_site(sn_2900_1, site_usa_ca, dnac_ticket)
    assign_device_site(sn_2900_2, site_usa_ca, dnac_ticket)

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
