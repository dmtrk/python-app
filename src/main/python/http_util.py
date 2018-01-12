import urllib.request


def do_post(url, data):
    print("do_post(" + url + ") data.len: " + str(len(data)))
    req = urllib.request.Request(url+"?y=0")
    req.add_header('User-Agent', 'urllib')
    req.add_header('Content-Type', 'text/plain')
    with urllib.request.urlopen(req, data.encode('utf-8')) as f:
        print(f.read().decode('utf-8'))
