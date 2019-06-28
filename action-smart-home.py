#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI ="config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage,conf)

def action_wrapper(hermes, intentMessage,conf):
#    result_sentence = intentMessage.intent.intent_name    ###say out the intent name
#    result_sentence = str(intentMessage.slots)            ###say something which i dun understand
#    result_sentence = intentMessage.slots.Corridor_lights.first().value ###extract the slot value from spoken text
    result_sentence = intentMessage.slots.Action.first().value + intentMessage.slots.Corridor_lights.first().value
    print("{}".format(intentMessage.intent.intent_name))
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id,result_sentence)

if __name__ =="__main__":
    mqtt_opts = MqttOptions()
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Superbigfatdaddy:Smart-Home",subscribe_intent_callback).start()

