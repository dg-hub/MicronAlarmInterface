# MicronAlarmInterface
A Python interface for controlling Mircon Meridian Alarm Systems over HTTP

Copyright (c) 2019 Daniel G - https://github.com/dg-hub



MicronAlarmInterface is a simple program for controling Mircon Meridian Alarm Systems over HTTP, it is based on reverse engineering the Javascript and HTTP requests performed by the embedded Web Interface.

# Features
MicronAlarmInterface has limited inital features, more can be added in future if required (please get in touch)

* Metadata.  Get Zone/Area Names
* Control.  Toggle Area arming status (Arm/Disarm)
* Status.  Get boolean status of Zones(Active) and Areas(Armed)

# Release Notes

Version 0.1.3 (December 16, 2019) Add initial code to control areas, get zone/area status and retreive metadata (Zone/Area names)

# Usage

After importing the module create a `MicronAlarmInterface` class:

```
import micron_interface

mci = micron_interface.MicronAlarmInterface("config.json")

#Get some Names and Status 
area_names = mci.get_area_names()
area_status = mci.get_area_status()
print("Area Status {}".format(area_status))

#Arm the Main Area
print("Arm Default Area ({})".format(area_names[1])
area_status = mci.set_area_name(area_names[1])
print("Area Status {}".format(area_status))

#Disarm the Main Area
print("Disarm Default Area ({})".format(area_names[1])
area_status = mci.set_area_name(area_names[1])
print("Area Status {}".format(area_status))
```

Note that the alarm status is updated only after a `set` request or when `update_xml_status()` is called


