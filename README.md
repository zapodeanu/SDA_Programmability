 - This code will get a switch hostname from a Catalyst 9300 using NETCONF.
 - The user will be asked to input a maximum air inlet temperature threshold for normal operation.
   If no user input, the code will use the default temperature - 46 Celsius.
 - The code has an infinite loop to check the switch inlet air temperature. It will collect the switch temperature and temperature sensor state using NETCONF.
   The loop will continue as long as the inlet air temperature will be lower that the threshold.
 - When the temperature exceeds the threshold, we will find out the interfaces in an operational state "up", and interfaces IP addresses.
 - The script will collect from weather.gov, using the REST APIs, the outdoor temperature for the location where the switch is located.
 - The temperature info, switch hostname, and IP addresses for "up" interfaces will be tweeted using 
the REST APIs from twitter.com