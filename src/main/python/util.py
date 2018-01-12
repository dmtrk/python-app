import os
import traceback
import subprocess

SECRETS_DIR = "/run/secrets/"
DONE_FOLDER = "Done"
ERROR_FOLDER= "Error"

def findConfigFile(args):
    if len(args) > 1:
        return args[1]
    # look for *.cfg file in secrets
    if os.path.isdir(SECRETS_DIR):
        for file in os.listdir(SECRETS_DIR):
            if file.endswith(".cfg"):
                return os.path.join(SECRETS_DIR,file)
    # look for *.cfg file in current directory
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".cfg"):
            return os.path.join(cwd,file)
    # default
    return os.path.join("/","config.cfg")


def parseProperties(stream) -> dict:
    p = dict()
    for line in stream.readlines():
        keyval = line.split("=")
        if len(keyval) > 1:
            p[keyval[0].strip()] = keyval[1].strip()
    return p


def getStr(dict, key, default_value) -> str:
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
        return value.upper() == "TRUE" if len(value) > 0 else default_value
    except Exception:
        print(traceback.format_exc())
    return default_value


def print_ip():
    p = subprocess.Popen(["netstat", "-nr"], stdout=subprocess.PIPE)
    out = p.stdout.read()
    print(out)

def shutdown(imap_client):
    print("shutdown() imap_client: " + str(imap_client))
    try:
        if imap_client != None:
            imap_client.logout()
            imap_client.shutdown()
    except Exception as e:
        print(e)

def select_folder(imap_client, folder):
    print("select_folder("+folder+"): " + str(imap_client))
    typ, data = imap_client.select(folder)
    print('Response code:', typ)
    if typ == 'OK':
        imap_client.create(folder+"/"+DONE_FOLDER)
        imap_client.create(folder+"/"+ERROR_FOLDER)
    else:
        raise LookupError("Invalid folder: '"+folder+"'")

def copy_to_done(imap_client, id, folder):
    print("Copy message "+str(id)+" to '"+folder+"/"+DONE_FOLDER+"'")
    typ, data = imap_client.uid('copy', id, folder+"/"+DONE_FOLDER)
    if typ != 'OK':
        print('Response:' + str(data))

def copy_to_error(imap_client, id, folder):
    print("Copy message "+str(id)+" to '"+folder+"/"+ERROR_FOLDER+"'")
    typ, data = imap_client.uid('copy', id, folder+"/"+ERROR_FOLDER)
    if typ != 'OK':
        print('Response:' + str(data))
