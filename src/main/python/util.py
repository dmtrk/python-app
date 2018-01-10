def parseProperties(stream) -> dict:
    p = dict()
    try:
        for line in stream.readlines():
            keyval = line.split("=")
            if len(keyval)>0:
                p[keyval[0].strip()] = keyval[1].strip()
    except IOError as e:
        raise
    return p