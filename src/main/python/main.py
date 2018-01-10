import datetime
import sys
import time

from util import parseProperties


def main():
    print('Connector arguments:', str(sys.argv))
    cfg = sys.argv[1] if len(sys.argv) > 1 else "/config.cfg"
    print("Loading configFile: '"+cfg+"'")

    p = parseProperties(open(cfg,"r"))
    print("p: '"+str(p)+"'")

    while 1 == 1:
        print("Hello, World! " + datetime.datetime.utcnow().isoformat())
        time.sleep(5)


if __name__ == '__main__':
    main()
