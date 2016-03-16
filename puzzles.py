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
    monte carlo approximation of the items to include in a knapsack with a clever init
    takes a list of tuples containing the value and weight of an item [(1, 2), (2, 3)]
    returns the total value optimal content
    '''
    # test case
    # items = [(1, 3), (3, 3), (5, 3), (4, 2), (3, 2), (1, 2), (2, 2), (3, 3), (5, 5)]
    # cap = 10
    # mc_trials = 15 
    # print best_knapsack(items, cap, mc_trials)

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


def max_stock_profit(prices):
    '''
    returns the greatest possible profit from a single long position
    takes a chronologically ordered list of prices
    returns the largest difference
    '''
    # test case
    # prices = [10, 7, 5, 8, 11, 9]
    top_profit = 0
    for i, price in enumerate(prices):
        profit = max(prices[i:]) - price
        if profit > top_profit:
            top_profit = profit
    return top_profit
         
def product_index(entries):
    '''
    for each item, find the product of every other item
    '''
    # test case
    # entries =  [1, 7, 3, 4]
    products = []
    for i, _ in enumerate(entries):
        factors = entries[:i] + entries[i + 1:]
        product = 1
        for factor in factors:
            product *= factor
        products.append(product)
    return products

if __name__ == '__main__':
    pass
