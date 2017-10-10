 get_netconf_9300_info.py:
 
 - This code will get a switch hostname from a Catalyst 9300 using NETCONF.
 - The user will be asked to input a maximum air inlet temperature threshold for normal operation.
   If no user input, the code will use the default temperature - 46 Celsius.
 - The code has an infinite loop to check the switch inlet air temperature. It will collect the switch temperature and temperature sensor state using NETCONF.
   The loop will continue as long as the inlet air temperature will be lower that the threshold.
 - When the temperature exceeds the threshold, we will find out the interfaces in an operational state "up", and configured IP addresses for up interfaces.
 - The script will collect using the REST APIs from weather.gov, the outdoor temperature for the location where the switch is located.
 - The temperature info, switch hostname, and IP addresses for "up" interfaces will be tweeted using the REST APIs from twitter.com
 
 dnac_apis.py
 
 - The script will create new areas, buildings, floors using data provided in .csv format. It will use google geo-location APIs to map the addresses to tghe coordinates needed to create the locations in DNA Center.
 - The roadmap for this script is to import the location info from Prime Infrastructure and become part of a migration tool
