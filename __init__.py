#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_VI/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .NKS import NKS

def create_instance(c_instance):
    return NKS(c_instance=c_instance)
