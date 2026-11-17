#!/usr/bin/env python3
import sys
import json
import csv
from datetime import datetime, timezone

from Evtx.Evtx import Evtx
from lxml import etree

from collections import Counter

MicrosoftSchema = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}
fields = ["source", "event_id", "provider", "timestamp", "computer", "level", "usersid", "processid", "threadid", "data"]


def _to_utc(dt):
    """Treat naive datetimes as UTC so they compare with record timestamps."""
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def parse_record(parsing):
    """Turn one python-evtx record into a flat dict."""
    root = etree.fromstring(parsing.xml().encode())
    system = root.find("e:System", MicrosoftSchema)

    def attr(tag, name):
        el = system.find(f"e:{tag}", MicrosoftSchema)
        return el.get(name) if el is not None else None

    data = {}
    for i, d in enumerate(root.findall(".//e:EventData/e:Data", MicrosoftSchema)):
        data[d.get("Name") or f"Data[{i}]"] = d.text

    return {
        "source": parsing.record_num(),
        "event_id": system.findtext("e:EventID", namespaces=MicrosoftSchema),
        "provider": attr("Provider", "Name"),
        "timestamp": attr("TimeCreated", "SystemTime") or str(parsing.timestamp()),
        "computer": system.findtext("e:Computer", namespaces=MicrosoftSchema),
        "level": system.findtext("e:Level", namespaces=MicrosoftSchema),
        "usersid": attr("Security", "UserID"),
        "processid": attr("Execution", "ProcessID"),
        "threadid": attr("Execution", "ThreadID"),
        "data": data,
    }


def evtx_reader(path, fromdate=None, todate=None):
    """Yield parsed records from an .evtx file, optionally filtered by datetime range."""
    fromdate, todate = _to_utc(fromdate), _to_utc(todate)
    with Evtx(path) as log:
        for parsing in log.records():
            if fromdate or todate:
                ts = _to_utc(parsing.timestamp())
                if fromdate and ts < fromdate:
                    continue
                if todate and ts > todate:
                    continue
            yield parse_record(parsing)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <file.evtx>")
    for event in evtx_reader(sys.argv[1]):
        print(json.dumps(event))
