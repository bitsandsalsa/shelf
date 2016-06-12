#!/usr/bin/env python
import argparse

from shelf import app

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--host', default='10.0.3.1', help='host address to server from')
parser.add_argument('-p', '--port', default=8000, type=int, help='TCP port to serve from')
args = parser.parse_args()
app.run(args.host, args.port)
