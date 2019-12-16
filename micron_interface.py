import enum
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import time
import json
import os
import logging

required_config = ["http_url", "http_username", "http_password"]

def load_config(filename):
    """Loads JSON config file and returns a Dictionary

    Returns:
    {str: str}: Dictionary of str values with configuration
    """
    try:
        with open('{}'.format(filename)) as json_data_file:
            config = json.load(json_data_file)
        logging.info('{} imported'.format(filename))
        for key in required_config:
            if key not in config:
                raise LookupError("config value '{}' missing from file: '{}'".format(key, filename))
        return config

    except FileNotFoundError:
        logging.error('FileNotFoundError: {}'.format(filename))


class Micron_Xml_Pointer(enum.IntEnum):
    """Return XML Element Text by using sequence value"""
    area_status = 251
    area_names = 178
    zone_status = 245
    zone_names = 182

class MicronAlarmInterface:

    config = {}
    xml_status = {}

    # XML Data Processing

    def update_xml_status(self):
        """Update the current state by retreiving from Alarm - GET request"""
        response = requests.get(self.config["http_url"], auth=HTTPBasicAuth(self.config["http_username"], self.config["http_password"]))
        self.xml_status = response.content

    def get_xml_element(self, xml_id):
        """Return XML Element Text by using sequence value"""
        tree = ET.fromstring(self.xml_status)
        return tree[xml_id].text

    def get_xml_element_tag(self, xml_id):
        """Return XML Element Tag by using sequence value"""
        tree = ET.fromstring(self.xml_status)
        return tree[xml_id].tag

    # Reference Data

    def get_area_names(self):
        """Gets the and Array of Area Names

        Returns:
        [str]: Array of str values with Area Names
        """
        area_names = []
        for i in range(0,4):
            ar = self.get_xml_element(Micron_Xml_Pointer.area_names + i)
            area_names.append(ar.strip())
        return area_names 

    def get_zone_names(self):
        """Gets the and Array of Zone Names

        Returns:
        [str]: Array of str values with Zone Names
        """
        zone_names = []
        for i in range(0,16):
            zn = self.get_xml_element(Micron_Xml_Pointer.zone_names + i)
            zone_names.append(zn.strip())
        return zone_names 

    # Status Data

    def get_zone_status(self):
        """Gets the status(bool) of all zones

        Returns:
        dict{str: bool}: Dictionary object containing of bool values with Zone Name as key
        """
        raw_zone_status = int(self.get_xml_element(Micron_Xml_Pointer.zone_status))
        zone_info = {}
        zone_names = self.get_zone_names()
        for zone_id, zone_name in enumerate(zone_names):
            zone_info[zone_name] = bool(raw_zone_status & (1 << zone_id))
        return zone_info

    def get_area_status(self):
        """Gets the status(bool) of all Areas - Armed{True}/Disarmed{False}

        Returns:
        dict{str: bool}: Dictionary object containing of bool values with Area Name as key
        """
        raw_area_status = int(self.get_xml_element(Micron_Xml_Pointer.area_status))
        area_info = {}
        area_names = self.get_area_names()
        for area_id, area_name in enumerate(area_names):
            area_info[area_name] = bool(raw_area_status & (1 << area_id))
        return area_info

    # Control Functions

    def set_area_id(self, area_id):
        """Toggle the state of a Area using the ID (Area 1 == ID:0) - Armed{True}/Disarmed{False}

        Returns:
        dict{str: bool}: Dictionary object containing of bool values with Area Name as key
        """
        padded_area_id = '%02d' % area_id
        area_request = "<?xml version='1.0' encoding='ISO-8859-1' ?><M><----------AA-->{}</----------AA--></M>".format(padded_area_id)
        header_obj = {'Content-Type': 'text/xml'}
        self.xml_status  = requests.post(self.config["http_url"], headers=header_obj, data = area_request, auth=HTTPBasicAuth(self.config["http_username"], self.config["http_password"])).content
        area_status = self.get_area_status()
        return area_status

    def set_area_name(self, area_name):
        """Toggle the state of a Area using the Name - Armed{True}/Disarmed{False}

        Returns:
        dict{str: bool}: Dictionary object containing of bool values with Area Name as key
        """
        area_name_array = self.get_area_names()
        area_id = area_name_array.index(area_name)
        return self.set_area_id(area_id)

    def __init__(self,config_filename="config.json"):
        """Constructor for class MicronAlarmInterface 

        Parameters:
        config_filename (str): the file location of config JSON file

        """
        self.config = load_config(config_filename)
        self.update_xml_status()

