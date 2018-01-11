import email
import email.header
import imaplib
import sys
import time

from util import *

DONE_FOLDER = "Done"
ERROR_FOLDER = "Error"

imap_client = None


def process_mail(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            # print part.as_string()
            continue
        if part.get('Content-Disposition') is None:
            # print part.as_string()
            continue
        file_name = part.get_filename()

        if bool(file_name):
            print("file_name: " + file_name)
            print("data: " + part.as_string())

            # filePath = os.path.join(detach_dir, 'attachments', fileName)
            # if not os.path.isfile(filePath) :
            # print fileName
            # fp = open(filePath, 'wb')
            # fp.write(part.get_payload(decode=True))
            # fp.close()





            # decode = email.header.decode_header(msg['Subject'])[0]
            # subject = decode[0]
            # print('subject: ' + subject)
            # print 'Raw Date:', msg['Date']


def create_done_error_folders(folder):
    if folder.upper() == "INBOX":
        imap_client.select()
    else:
        imap_client.select(folder)
    # create folders
    imap_client.create(DONE_FOLDER)
    imap_client.create(ERROR_FOLDER)
    typ, data = imap_client.list()
    print('Response code:', typ)
    print('Response:' + str(data))


def check_mail():
    print("check_mail() imap_client: " + str(imap_client))
    try:
        typ, data = imap_client.uid('search', None, 'UNDELETED')
        if typ == 'OK':
            for uid in data[0].split():
                print("Getting message ", uid)
                try:
                    rv, data = imap_client.fetch(uid, '(RFC822)')
                    if rv != 'OK':
                        print("ERROR getting message", uid)
                        imap_client.copy(uid, ERROR_FOLDER)
                    else:
                        msg = email.message_from_bytes(data[0][1])
                        process_mail(msg)
                        imap_client.copy(uid, DONE_FOLDER)
                except Exception:
                    print(traceback.format_exc())
                    imap_client.copy(uid, ERROR_FOLDER)
                # update message status
                imap_client.store(uid, '+FLAGS', r'\Deleted')
            # remove messages from folder
            imap_client.expunge()
        else:
            print("No messages found!")

    except Exception:
        print(traceback.format_exc())


# Main logic
try:
    print('Connector arguments:', str(sys.argv))
    print_ip()
    config_file = findConfigFile(sys.argv)
    print("Loading config_file: '" + config_file + "'")
    properties = parseProperties(open(config_file, "r"))
    # print("p: '"+str(p)+"'")
    poll_int= getInt(properties, "imap.poll.interval", 60)
    host    = getStr(properties, "imap.host", "127.0.0.1")
    port    = getInt(properties, "imap.port", 143)
    port_ssl= getInt(properties, "imap.port_ssl", 993)
    user    = getStr(properties, "imap.username", "")
    password= getStr(properties, "imap.password", "")
    folder  = getStr(properties, "imap.folder", "INBOX")
    usessl  = getBool(properties,"imap.usessl", True)
    keyfile = getStr(properties, "imap.keyfile", "key.pem")
    certfile= getStr(properties, "imap.certfile", "cert.pem")
    if len(user) == 0 or len(password) == 0:
        raise Exception("'imap.username' and 'imap.password' are required")

    while 1 == 1:
        try:
            # print("Hello, World! " + datetime.datetime.utcnow().isoformat())
            if imap_client is None:
                if usessl:
                    print("Connecting to 'imaps://" + host + ":" + str(port_ssl) + "' as '" + user + "'")
                    imap_client = imaplib.IMAP4_SSL(host, port, keyfile, certfile)
                else:
                    print("Connecting to 'imap://" + host + ":" + str(port) + "' as '" + user + "'")
                    imap_client = imaplib.IMAP4(host, port)
                # login
                imap_client.login(user, password)
                create_done_error_folders(folder)
            else:
                imap_client.noop()
            # check_mail
            check_mail()
        except ConnectionRefusedError:
            print("Unable to connect to '" + host + ":" + str(port) + "' as '" + user + "'")
            shutdown(imap_client)
            imap_client = None
        except Exception:
            print(traceback.format_exc())
            shutdown(imap_client)
            imap_client = None
        # sleep
        time.sleep(poll_int)

except Exception:
    print(traceback.format_exc())
finally:
    shutdown(imap_client)
