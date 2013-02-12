#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import random
import datetime

def get_breakups():
    f = open('nenana_converted.txt')
    breakups = {}
    for line in iter(f):
        line_array = line.split(',')
        date = line_array[0]
        month = date.split()[0]
        day = date.split()[1]
        clock_time = date[(len(day) + 1 + len(month) + 1):]
        year = line_array[1].strip("\n")
        breakups[year] = "%s/%s/%s %s" % (month, day, year, clock_time)
    f.close()
    return breakups

breakups = get_breakups()

FMT = '%m/%d/%Y %I:%M %p'

YEAR = '2009'
ACTUAL = breakups[YEAR]
ACTUAL = datetime.datetime.strptime(ACTUAL, FMT)

MIN = "4/20/%s 4:54 PM" % YEAR
MAX = "5/20/%s 11:41 AM" % YEAR

MAX = datetime.datetime.strptime(MAX, FMT)
MIN = datetime.datetime.strptime(MIN, FMT)
DIFF = MAX - MIN
MINUTES = divmod(DIFF.total_seconds(), 60)[0]
MEAN = MIN + datetime.timedelta(minutes=MINUTES/2)

# print MEAN.strftime(FMT)

def make_guess():
    guess_delta = (random.gauss(0,.5) * MINUTES/4)
    guess = MEAN + datetime.timedelta(minutes=guess_delta)
    return guess.replace( second=0, microsecond=0)

random_datetimes = []
guesses = 0
while guesses < 1000:
    guess = make_guess()
    # want 1000 unique guesses
    if guess not in random_datetimes:
        random_datetimes.append( guess )
        guesses++

guess_diffs = []    
for guess in random_datetimes:
    # print guess.strftime(FMT) 
    guess_diff = guess - ACTUAL
    guess_minutes = divmod(guess_diff.total_seconds(), 60)[0]
    # print guess_minutes
    guess_diffs.append( abs(guess_minutes) )

average = sum( guess_diffs ) / len(guess_diffs)

# print    
# print "off by"
# print average
# print "minutes"
# print
# print "off by"
# print average / 60 
# print "hours"    
# print
# print "worst guess:"
# print max(guess_diffs)
print
print "closest guess:"
print min(guess_diffs)
print ACTUAL.strftime(FMT) 
print ACTUAL in random_datetimes

if ACTUAL in random_datetimes:
    guesses_file = open( 'guesses.txt', 'w' )
    for guess in random_datetimes:
        guesses_file.write( guess.strftime(FMT) + "\n" )
    guesses_file.close()
    
