#! /usr/bin/env python

import argparse
import random
import string
import os
import sys
import re
from urlparse import urlparse

thisdir = os.path.dirname(__file__)
libdir = os.path.abspath(os.path.join(thisdir, '../src'))
if libdir not in sys.path:
    sys.path.insert(0, libdir)

from reservoir_sampler import ReservoirSampler
from stream_iterator import StreamIterator

DEFAULT_SOURCE_LENGTH = 1000


def get_random_string(length):
    str = ''.join(random.choice(string.lowercase) for x in range(length))
    print "Random str: %s" % str
    return str


def uri_validator(x):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(x)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', nargs='?',
                    help='Input data (string, url)')
parser.add_argument('-l', '--length', type=int, default=5,
                    help='Sample length, default 5')
parser.add_argument('-r', '--random', action='store_true',
                    help='Use random string as input')
args = parser.parse_args()

if not sys.stdin.isatty():
    stream_input = sys.stdin.read()
    print "Input Stream: %s" % stream_input
    iterator = list(stream_input).__iter__()

elif args.random:
    iterator = list(get_random_string(DEFAULT_SOURCE_LENGTH)).__iter__()
else:
    if args.input:

        if uri_validator(args.input):
            iterator = StreamIterator(args.input).get_iterator()
        else:
            iterator = list(args.input).__iter__()
    else:
        iterator = StreamIterator('php://stdin').get_iterator()


sampler = ReservoirSampler(iterator)
print "----------------------------------------------"
print "%s \n" % ''.join(sampler.get_sample(args.length))
