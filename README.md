 **get_netconf_9300_info.py**:
 
 - This code will get a switch hostname from a Catalyst 9300 using NETCONF.
 - The user will be asked to input a maximum air inlet temperature threshold for normal operation.
   If no user input, the code will use the default temperature - 46 Celsius.
 - The code has an infinite loop to check the switch inlet air temperature. It will collect the switch temperature and temperature sensor state using NETCONF.
   The loop will continue as long as the inlet air temperature will be lower that the threshold.
 - When the temperature exceeds the threshold, we will find out the interfaces in an operational state "up", and configured IP addresses for up interfaces.
 - The script will collect using the REST APIs from weather.gov, the outdoor temperature for the location where the switch is located.
 - The temperature info, switch hostname, and IP addresses for "up" interfaces will be tweeted using the REST APIs from twitter.com
 
 **dnac_apis.py**
 
 - This application will use the DNA Center REST APIs to create two new areas, three new sites, one floor.
 - It will use the Google Geolocation APIs to map addresses to their longitude and latitude coordinates required
    by DNA Center during the configuration of new sites.
 - It will continue by assigning devices based on the Serial Numbers to each of these sites.
 - All the data required by this sample code could be easily imported from a CSV file.

 **delta-spark.py**
 
 - This application will run on IOS XE Guest Shell and detect when a configuration change occurs on the device
 - It will identify the difference between a baseline configuration and the updated running configuration
 - The device hostname will be identified
 - The device hostname and configuration delta will be posted to Spark Room, to notify about the change