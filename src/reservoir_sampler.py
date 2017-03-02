import random


class SamplerInterace(object):

    def get_sample(self, strlen):
        return NotImplemented


class ReservoirSampler(SamplerInterace):

    def __init__(self, iterator):
        self.iterator = iterator

    def get_sample(self, strlen):

        result = []
        N = 0

        for item in self.iterator:
            #print "ITEM : %s" % item
            N += 1
            if N <= strlen:
                result.append(item)
            elif N > strlen and random.random() < strlen / float(N + 1):
                replace = random.randint(0, len(result) - 1)
                result[replace] = item

        return result
