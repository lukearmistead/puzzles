from __future__ import division
from random import shuffle


def top_tweets(tweets, top):
    '''returns the most common <top> entries from a list of tweets'''
    # test case
    # tweets = ['a', 'a', 'b', 'c', 'u', 'c']
    # print bar(tweets, 2)
    dtweets = dict.fromkeys(tweets, 0)
    for tweetkey in dtweets:
        for tweet in tweets:
            if tweetkey == tweet:
                dtweets[tweetkey] += 1
    dtweets = [(v, k) for k, v in dtweets.iteritems()]
    dtweets = sorted(dtweets, reverse=True)[:top]
    return [tweet[1] for tweet in dtweets]


def best_knapsack(items, cap, mc_trials):
    '''
    approximates the to include in a knapsack
    takes a list of tuples containing the value and weight of an item [(1, 2), (2, 3)]
    returns the total value optimal content
    '''
    best_bag = _try_knapsack(sorted(items, key=lambda item: item[0] / item[1], reverse=True))
    for iteration in xrange(mc_trials):
        shuffle(items)
        try_bag = _try_knapsack(items)
        if try_bag[0] > best_bag[0]:
            best_bag = try_bag
    return best_bag


def _try_knapsack(items):
    '''
    knapsack helper function that returns the value and contents of the sum of 
    the ordered items
    '''
    bag_value = 0
    bag_weight = 0
    bag = []
    for item in items:
        if bag_weight + item[1] <= cap:
            bag_value += item[0]
            bag_weight += item[1]
            bag.append(item)
    return bag_value, bag


if __name__ == '__main__':
    items = [(1, 3), (3, 3), (5, 3), (4, 2), (3, 2), (1, 2), (2, 2), (3, 3), (5, 5)]
    cap = 10
    mc_trials = 15 

    best_bag = try_knapsack(sorted(items, key=lambda item: item[0] / item[1], reverse=True))
    for iteration in xrange(mc_trials):
        shuffle(items)
        try_bag = try_knapsack(items)
        if try_bag[0] > best_bag[0]:
            best_bag = try_bag
            print 'new best bag:'
            print best_bag

