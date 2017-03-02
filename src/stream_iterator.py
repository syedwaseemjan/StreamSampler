import urllib2


class IteratorInterface(object):

    def get_iterator(self):
        return NotImplemented


class StreamIterator(IteratorInterface):

    def __init__(self, url):
        self.url = url

    def get_iterator(self):
        print "get iterator called"
        try:
            data = urllib2.urlopen(self.url)
            for line in data:
                yield line
        except urllib2.URLError, err:
            from traceback import print_exc
            print print_exc(err.reason)
        finally:
            try:
                data.close()
            except NameError:
                pass
