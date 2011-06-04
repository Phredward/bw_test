"""Simple bandwidth tester
(C) Fred Blau 2010
"""
import array
import optparse
import time
import socket
try:
    range=xrange
except NameError:
    pass

PORT=12345

#1kdata = 1024 Bytes
data1k='1234567890'.encode('utf8')
data1k=data1k*10
data1k=data1k*10
data1k=data1k+'123456789012345678901234'.encode('utf8')
data16k = data1k*16
data1M = data1k*1024
data4M = data1M * 4
data16M = data1M*16

def print_human(bytes):
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fTB' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.3fGB' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.3fMB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.3fKB' % kilobytes
    else:
        size = '%.0fB' % bytes
    return size

def init_options():
    global options, args
    parser = optparse.OptionParser()
    parser.add_option("--connect")
    parser.add_option("--port", default=PORT, type="int", help="port to connect to or listen on")
    parser.add_option("--time-to-run", default=20, type="int", help="XX seconds of upload, and XX seconds of download time")
    options, args = parser.parse_args()

def do_connect(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return (s,None)

def do_listen(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(1)
    print('listening on port %d' % port)
    conn, addr = s.accept()
    return (conn,addr)

def do_recv(s, duration=0):
    if duration:
        s.send(str(duration).encode('utf8'))
    start_time=time.time()
    second_time=start_time
    cur_time = start_time
    count=0
    d=array.array('b')
    d.append(0)
    for i in range(16):
        d.extend(d)
    #print(len(d))
    #instead of printing the length of the receive buffer, there should be
    #blocksize constants and the send and recieve buffer should be the same
    #(see hardcoded recv_into below)
    while True:
        len_r=s.recv_into(d, 16*1024)
        count += len_r
        cur_time=time.time()
        if cur_time-second_time > 1.0:
            print('bw: %s' % print_human(count / (cur_time - second_time)))
            count=0
            second_time = cur_time
        if d[len_r-4:len_r].tostring() == 'done'.encode('utf8'):
            return

def do_send(s, duration=0):
    if not duration:
        d=s.recv(100)
        duration = float(d)
    start_time=second_time=cur_time=time.time()
    count_len = len(data16k)
    count=0
    while cur_time - start_time < duration:
        s.send(data16k)
        count += count_len
        cur_time = time.time()
        if cur_time - second_time > 1.0:
            print('bw: %s' % print_human(count / (cur_time - second_time)))
            count=0
            second_time = cur_time
    s.send('done'.encode('utf8'))


init_options()
print('start')
if options.connect:
    (s, _) = do_connect(options.connect, options.port)
    do_recv(s, options.time_to_run)
    print('and now send')
    do_send(s, options.time_to_run)
else:
    (s, remote_host) = do_listen(options.port)
    print('connection from %s:%d' % (remote_host[0], remote_host[1]))
    do_send(s)
    time.sleep(2)
    print('and now recv')
    do_recv(s)
