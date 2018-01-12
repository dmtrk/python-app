import email
import email.header
import imaplib
import ssl
import sys
import time

from http_util import do_post
from imap_util import *

imap_client = None


def process_mail(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            # print part.as_string()
            continue
        if part.get('Content-Disposition') is None:
            # print part.as_string()
            do_post(post_url, part.get_content_maintype())

        #file_name = part.get_filename()

        #if bool(file_name):
            #print("file_name: " + file_name)
            #print("data: " + part.as_string())

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


def check_mail(folder):
    print("check_mail() imap_client: " + str(imap_client))
    try:
        imap_client.select(folder)
        typ, data = imap_client.uid('search', None, 'UNDELETED')
        print('Response code:', typ)
        if typ == 'OK':
            for id in data[0].split():
                print("Getting message ", id)
                try:
                    typ, data = imap_client.uid('fetch', id, '(RFC822)')
                    if typ == 'OK':
                        msg = email.message_from_bytes(data[0][1])
                        process_mail(msg)
                        copy_to_done(imap_client, id, folder)
                    else:
                        print('Response:' + str(data))
                        raise Exception("ERROR getting message '" + id + "'")
                except Exception:
                    print(traceback.format_exc())
                    copy_to_error(imap_client, id, folder)
                # update message status
                imap_client.uid('store', id, '+FLAGS', r'\Deleted')
            # end for
            # remove messages from folder
            imap_client.expunge()
        else:
            print("No messages found!")
    except Exception:
        print(traceback.format_exc())


# Main logic
try:
    print("Python version: "+str(sys.version))
    print("Connector arguments:'"+str(sys.argv)+"'")
    print_ip()
    config_file = findConfigFile(sys.argv)
    print("Loading config_file: '" + config_file + "'")
    properties = parseProperties(open(config_file, "r"))
    # print("p: '"+str(p)+"'")
    poll_int = getInt(properties, "imap.poll.interval", 60)
    host = getStr(properties, "imap.host", "127.0.0.1")
    port = getInt(properties, "imap.port", 143)
    port_ssl = getInt(properties, "imap.port_ssl", 993)
    user = getStr(properties, "imap.username", "")
    password = getStr(properties, "imap.password", "")
    folder = getStr(properties, "imap.folder", "INBOX")
    usessl = getBool(properties, "imap.usessl", True)
    keyfile = getStr(properties, "imap.keyfile", "key.pem")
    certfile = getStr(properties, "imap.certfile", "cert.pem")
    post_url = getStr(properties, "http.post_url", "")
    if len(user) == 0 or len(password) == 0:
        raise Exception("'imap.username' and 'imap.password' are required")

    while 1 == 1:
        try:
            # print("Hello, World! " + datetime.datetime.utcnow().isoformat())
            if imap_client is None:
                if usessl:
                    print("Connecting to 'imaps://" + host + ":" + str(port_ssl) + "' as '" + user + "'")
                    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                    imap_client = imaplib.IMAP4(host, port)
                    imap_client.starttls(ctx)
                else:
                    print("Connecting to 'imap://" + host + ":" + str(port) + "' as '" + user + "'")
                    imap_client = imaplib.IMAP4(host, port)
                # login
                imap_client.login(user, password)
                select_folder(imap_client, folder)
            else:
                imap_client.noop()
            # check_mail
            check_mail(folder)
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
