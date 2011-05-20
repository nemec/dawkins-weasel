import heapq
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import dawkins_weasel
import base

genfunc = dawkins_weasel.generate

# http://bytesizebio.net/index.php/2011/04/23/shakespeares-birthday-and-evolution/
#genfunc = base.loopweasel


num_reps = 10

class RollingAverage(object):
  def __init__(self, seed):
    self.sum = float(seed)
    self.num = 1

  def addall(self, seq):
    for i in seq:
      self.add(i)

  def add(self, val):
    self.sum = ((self.sum * self.num) + val) / (self.num + 1)
    self.num += 1

  def __str__(self):
    return str(self.sum)


class RollingMedian(object):
  def __init__(self, seed):
    self._med = seed
    self.min = []
    self.max = []

  def addall(self, *seq):
    if len(seq) == 1:
      seq = seq[0]
    for i in seq:
      self.add(i)

  def add(self, val):
    if val < self._med:
      heapq.heappush(self.min, -val)
      heapq.heappush(self.max, self._med)
    else:
      heapq.heappush(self.max, val)
      heapq.heappush(self.min, -self._med)

    if len(self.min) < len(self.max):
      self._med = heapq.heappop(self.max)
    else:
      self._med = -heapq.heappop(self.min)

  @property
  def median(self):
    if len(self.min) < len(self.max):
      return (self.max[0] + self._med) / 2.0
    elif len(self.max) < len(self.min):
      return (-self.min[0] + self._med) / 2.0
    else:
      return self._med

  def __str__(self):
    return str(self.median)


def variable_length(mn, mx, step = 1, ocount = 300):
  best = {}
  for length in xrange(mn, mx + 1, step):
    print "Testing string length {0}, offspring count {1}".format(length,ocount)
    for count in xrange(num_reps):
      gens = genfunc(dawkins_weasel.random_phrase(length),
                                      ocount, 0.05, verbose = False)
      if length not in best:
        best[length] = (RollingAverage(gens), RollingMedian(gens))
      else:
        best[length][0].add(gens)
        best[length][1].add(gens)
  return best

def variable_ocount(mn, mx, step = 50, length = 28):
  best = {}
  for ocount in xrange(mn, mx + 1, step):
    print "Testing string length {0}, offspring count {1}".format(length,ocount)
    for count in xrange(num_reps):
      gens = genfunc(dawkins_weasel.random_phrase(length),
                                      ocount, 0.05, verbose = False)
      if ocount not in best:
        best[ocount] = (RollingAverage(gens), RollingMedian(gens))
      else:
        best[ocount][0].add(gens)
        best[ocount][1].add(gens)
  return best

l = variable_length(10, 20)
oc = variable_ocount(100,1000, step=10)


fig = plt.figure(0)
plt.subplots_adjust(hspace=0.4)
font = FontProperties(size="medium")

sub1 = fig.add_subplot(211, title="Phrase Length v. Generations")
sub1.plot(sorted(l.keys()), [l[x][0].sum for x in l], label="Average")
sub1.plot(sorted(l.keys()), [l[x][1].median for x in l], label="Median")
plt.xlabel("Phrase Length")
plt.ylabel("Generations")
plt.legend(prop=font)

sub2 = fig.add_subplot(212, title="Offspring Count v. Generations")
sub2.plot(sorted(oc.keys()), [oc[x][0].sum for x in oc], label="Average")
sub2.plot(sorted(oc.keys()), [oc[x][1].median for x in oc], label="Median")
plt.xlabel("Offspring Count")
plt.ylabel("Generations")
plt.legend(prop=font)
plt.show()
