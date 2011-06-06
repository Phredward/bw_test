bw_test.py -- A Bandwidth Tester
================================

bw_test.py is a simple script that you run to test the bandwidht between two
endpoints.  The two endpoints can be anywhere where at least one side can
connect to the other, even on the same machine (although this really just tests cpu usage through the loopback interface).

The server will send data as hard as it can, then the client will send data as
hard as it can.  Bandwidth information is printed every second.

Instructions:
-------------

```
Usage: bw_test.py [options]

Options:
  -h, --help            show this help message and exit
  --connect=CONNECT
  --port=PORT           port to connect to or listen on
  --time-to-run=TIME_TO_RUN
                        XX seconds of upload, and XX seconds of download time
```

* start the server first with `python bw_test.py`
* start the client with `python bw_test.py --connect IP_OR_HOSTNAME`
