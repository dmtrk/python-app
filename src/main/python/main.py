import datetime
import imaplib
import sys
import time

from util import *


def main():
    print('Connector arguments:', str(sys.argv))
    imap_client = None
    try:
        config_file = findConfigFile(sys.argv)
        print("Loading config_file: '" + config_file + "'")
        properties = parseProperties(open(config_file, "r"))
        # print("p: '"+str(p)+"'")
        poll_interval = getInt(properties, "imap.poll.interval", 60)
        host = getString(properties, "imap.host", "127.0.0.1")
        port = getInt(properties, "imap.port", 143)
        user = getString(properties, "imap.username", "")
        password = getString(properties, "imap.password", "")
        usessl = getBool(properties, "imap.usessl", True)
        keyfile = getString(properties, "imap.keyfile", "key.pem")
        certfile= getString(properties, "imap.certfile", "cert.pem")
        if len(user) == 0 or len(password) == 0:
            raise Exception("'imap.username' and 'imap.password' are required")

        while 1 == 1:
            try:
                print("Hello, World! " + datetime.datetime.utcnow().isoformat())

                if imap_client is None:
                    print("Connecting to '" + host + ":" + str(port) + "' as '"+user+"'")
                    imap_client = imaplib.IMAP4_SSL(host,port,keyfile,certfile) if usessl else imaplib.IMAP4(host, port)
                    imap_client.login(user, password)
                else:
                    imap_client.noop()

                check_mail(imap_client)

            except ConnectionRefusedError:
                print("Unable to connect to '" + host + ":" + str(port) + "' as '"+user+"'")
                close(imap_client)
                imap_client=None
            except Exception:
                print(traceback.format_exc())
                close(imap_client)
                imap_client=None
            # sleep
            time.sleep(poll_interval)

    except Exception:
        print(traceback.format_exc())
    finally:
        close(imap_client)


def check_mail(imap_client):
    print("check_mail() imap_client: " + str(imap_client))
    try:
        typ, data = imap_client.list()
        print('Response code:', typ)
        print('Response:' + str(data))
    except Exception:
        print(traceback.format_exc())


def close(imap_client):
    print("close() imap_client: " + str(imap_client))


if __name__ == '__main__':
    main()
