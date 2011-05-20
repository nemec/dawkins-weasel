import re
import sys
import copy
import string
import random

alphabet = string.ascii_lowercase+' '

def random_phrase(length):
  return "".join(random.choice(alphabet) for _ in xrange(length))

def fitness(mutation, phrase):
  """ Returns Hamming Distance for two strings
      Must be same length
  """
  return sum(i != j for i,j in zip(mutation, phrase))

def generate(phrase, offspring_count = 300,
                  mut_rate = 0.05, verbose = True):
  phrase = re.sub("[^{0}]".format(alphabet), "", phrase.lower())
  length = len(phrase)
  offspring_count = int(offspring_count)
  mut_rate = float(mut_rate)

  gen = 1
  seed = random_phrase(length)
  fit = fitness(seed, phrase)

  while True:
    if verbose:
      print "Generation {0}:".format(gen), seed
    if fit == 0:
      break

    parent = list(seed)
    for child in xrange(offspring_count):
      # Generate mutations
      gene = copy.copy(parent)
      for x in xrange(length):
        if random.random() <= mut_rate:
          gene[x] = random.choice(alphabet)

      # Check fitness
      child_fit = fitness(gene, phrase)
      if child_fit < fit:
        seed = "".join(gene)
        fit = child_fit
    gen += 1
  return gen
    

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print "Usage: weasel target_string n_offspring mutation_rate"
    print
    print "target_string: the string you would eventually evolve into"
    print "n_offspring: number of offspring per generation"
    print "mutation_rate rate of mutation per position, 0=< m <1"
    sys.exit(1)
  target_string = sys.argv[1]
  n_offspring = int(sys.argv[2])
  mut_rate = float(sys.argv[3])

  generate(target_string, n_offspring, mut_rate)
  
