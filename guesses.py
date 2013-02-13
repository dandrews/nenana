#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import datetime
import random
import sys

FMT = '%m/%d/%Y %I:%M %p'

def get_breakups():
    f = open('nenana_converted.txt')
    breakups = []
    for line in iter(f):
        line_array = line.split(',')
        date = line_array[0]
        month = date.split()[0]
        day = date.split()[1]
        clock_time = date[(len(day) + 1 + len(month) + 1):]
        year = line_array[1].strip("\n")
        breakup_date = "%s/%s/%s %s" % (month, day, year, clock_time)
        breakups.append( datetime.datetime.strptime(breakup_date, FMT) )
    f.close()
    return breakups

breakups = get_breakups()

YEAR = 2011

index = map(lambda d: d.year, breakups).index(YEAR)
ACTUAL = breakups[index]

breakups = breakups[-30:]

breakups.sort(key = lambda d: (d.month, d.day))

MIN = breakups[0].replace( year=YEAR)
MAX = breakups[-1].replace( year=YEAR)

DIFF = MAX - MIN
MINUTES = divmod(DIFF.total_seconds(), 60)[0]
MEAN = MIN + datetime.timedelta(minutes=MINUTES/2)

print "ACTUAL: %s" % ACTUAL.strftime(FMT) 
print "MIN: %s" % MIN.strftime(FMT)
print "MEAN: %s" % MEAN.strftime(FMT)
print "MAX: %s" % MAX.strftime(FMT)
print

def flip(p):
    return -1 if random.random() < p else 1

def make_guess( method = '' ):
    if method == 'guass0,.5/4':
        guess_delta = (random.gauss(0,.5) * MINUTES/4)
        guess = MEAN + datetime.timedelta(minutes=guess_delta)
        return guess.replace( second=0, microsecond=0)
    else:
        # normal guass
        guess_delta = (random.gauss(0,1) * MINUTES/4)
        guess = MEAN + datetime.timedelta(minutes=guess_delta)
        return guess.replace( second=0, microsecond=0)

MAX_GUESSES = 1000

TEST_COUNT = 100

results = []
correct_guesses = 0
while len(results) < TEST_COUNT:
    
    random_datetimes = []
    while len(random_datetimes) < MAX_GUESSES:
    
        guess = make_guess('guass0,.5/4') 
    
        # want MAX_GUESSES unique guesses
        if guess not in random_datetimes:
            random_datetimes.append( guess )

    guess_diffs = []    
    for guess in random_datetimes:
        guess_diff = guess - ACTUAL
        guess_minutes = divmod(guess_diff.total_seconds(), 60)[0]
        guess_diffs.append( abs(guess_minutes) )

    results.append( min(guess_diffs) )

    if ACTUAL in random_datetimes:
        correct_guesses += 1
    
average = sum( results ) / len(results)

print "AVERAGE GUESS OFF BY: %s" % average
print
print "CORRECT GUESSES IN %s: %d" % ( TEST_COUNT, correct_guesses )
print

print "ACCURACY: {0:.0f}% ".format( ( float(correct_guesses) / TEST_COUNT ) * 100 )
print

sys.exit()

if ACTUAL in random_datetimes:
    guesses_file = open( 'guesses.txt', 'w' )
    for guess in random_datetimes:
        guesses_file.write( guess.strftime(FMT) + "\n" )
    guesses_file.close()
    
