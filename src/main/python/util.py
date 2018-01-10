def parseProperties(stream) -> dict:
    p = dict()
    try:
        for line in stream.readlines():
            keyval = line.split("=")
            p[keyval[0].strip()] = keyval[1].strip()
    except IOError as e:
        raise
    return p