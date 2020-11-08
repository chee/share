#!/usr/bin/env python
import random
from sys import argv

consonants = "bcdfghjklmnpqrstvwyz"
vowels = "aeiou"

def vowel():
	return random.choice(vowels)

def consonant():
	return random.choice(consonants)

def word():
	return ''.join([
		consonant(),
		vowel(),
		consonant(),
		vowel(),
		consonant()
	])

def getseq(length=1, words=[]):
	if length == 0:
		return '-'.join(words)
	else:
		return getseq(length - 1, [word()] + words)

if __name__ == "__main__":
	if len(argv) > 1:
		length = int(argv[1])
	else:
		length = 1
	print(getseq(length))
