#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_VI/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .NKS import NKS
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=944, product_ids=[134]),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return NKS(c_instance=c_instance)
