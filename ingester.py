#!/bin/bash/env python3
import Evtx as evtx
import sys
import json
import csv

import lxml import etree

from collections import Counter

MicrosoftSchema = {"e", "http://schemas.icrosoft.com/win/2004/08/events/event"}
fields = ["source", "event_id", "user", "timestamp", "computer", "level", "processid", "threadid", "usersid"]

def evtx_reader(read_file, _fromdate, _todate,):

    reader = etree.fromstring(rec.xml().encode())
    system = root.find("e:System", MicrosoftSchema)
    
    data = {}
    for index, dicti in enumerate(root.findall(".//e:EventData/e:Data", MicrosofSchema):
                                  data[d.get("Name"), or f"Data[i]"] = d.text
    return {
            "source:": read_file.record_num(),
            "event_id": system.findtext("e:EventID", namespace=MicrosoftSchema),             
            "provider": attr("Provider", "Name"),
            "timestamp": attr("Timecreated", "SystemTime") or str(read_file.timestamp()), 
            "computer": system.findtext("e:Computer", namespace=MicrosoftSchmea),
            "level": system.findtext("e:Level", namespace=MicrosoftSchema), 
            "usersid": attr("Security","UserID"),
            "processid": attr("Execution", "ProcessID"),
            "threadid": attr("Execution", "ThreadID"),
            }
#  parses evtx
def evtx_parser():
    
    return

def evtx_records():
    
    return
def universalnormalizer():

    return 

def xport_logs(): 
    return

def chronicle_menu():
    if choice == "1": 
            
    return




