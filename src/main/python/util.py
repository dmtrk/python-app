import os
import traceback


def findConfigFile(args):
    if len(args) > 1:
        return args[1]
    else:
        for file in os.listdir("/"):
            if file.endswith(".cfg"):
                return "/"+file
    return "/config.cfg"


def parseProperties(stream) -> dict:
    p = dict()
    for line in stream.readlines():
        keyval = line.split("=")
        if len(keyval) > 1:
            p[keyval[0].strip()] = keyval[1].strip()
    return p


def getString(dict, key, default_value) -> str:
    value = (dict[key] if key in dict else "").strip()
    return value if len(value) > 0 else default_value


def getInt(dict, key, default_value) -> str:
    try:
        value = (dict[key] if key in dict else "").strip()
        return int(value) if len(value) > 0 else default_value
    except Exception:
        print(traceback.format_exc())
    return default_value

def getBool(dict, key, default_value) -> str:
    try:
        value = (dict[key] if key in dict else "").strip()
        return value.upper()=="TRUE" if len(value) > 0 else default_value
    except Exception:
        print(traceback.format_exc())
    return default_value

