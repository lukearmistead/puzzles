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

def diagonal_difference(mat):
    ''' takes a square matrix and returns the absolute difference between the
    sums of its diagonals'''
    product = 1
    other_product = 1
    for i, row in enumerate(mat):
        product += row[i]
        other_product += row[len(row) - i - 1]
    return abs(product) - abs(other_product)

def rectangle_overlap(rec1, rec2):
    ''' takes the coordinates and dimensions of two rectangles as a dictionary
    and returns the coordinates and dimensions of the overlapping space
    input example:
    rec1 = {
        # coordinates of bottom-left corner
        'left_x': 0,
        'bottom_y': 5,
        # width and height
        'width': 10,
        'height': 10
    }
    rec2 = {
        # coordinates of bottom-left corner
        'left_x': 1,
        'bottom_y': 6,
        # width and height
        'width': 10,
        'height': 10
    }
    output example
    my_rectangle = {
        # coordinates of bottom-left corner
        'left_x': 1,
        'bottom_y': 5,
        # width and height
        'width': 10,
        'height': 4,
    }
    interviewcake.com/question/python/rectangular-love
    '''
    rec_out = {}
    # establish right and bottom coordinates for output rectangle (rec_out)
    rec_out['left_x'] = max(rec1['left_x'], rec2['left_x'])
    rec_out['bottom_y'] = max(rec1['bottom_y'], rec2['bottom_y'])
    # find the leftmost & top coordinates for input rectangles
    rec1['right_x'] = rec1['left_x'] + rec1['width']
    print rec1['right_x']
    rec1['top_y'] = rec1['bottom_y'] + rec1['height']
    print rec1['top_y']
    rec2['right_x'] = rec2['left_x'] + rec2['width']
    print rec2['right_x']
    rec2['top_y'] = rec2['bottom_y'] + rec2['height']
    print rec2['top_y']
    # get output rectangle dimensions
    rec_out['height'] = min(rec1['right_x'], rec1['right_x']) - rec_out['left_x']
    rec_out['width'] = min(rec1['top_y'], rec1['top_y']) - rec_out['bottom_y'] 
    return rec_out    

def _get_letters(numbers):
    """Helper function to return a list of the lists of letters associated with
    each number in the phone number
    """
    number_index = {
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }
    letters = [number_index[number] for number in numbers]
    return letters


def _get_letter_combis(output, remaining_letters):
    """Recursively finds all of the combinations of letters associated with
    each number in the entry
    """
    if not remaining_letters:
        return output
    letters = remaining_letters.pop()
    new_output = []
    if not output:
        new_output = letters
    else:
        for entry in output:
            for letter in letters:
                combi = entry + letter
                new_output.append(entry + letter)
    return _get_letter_combis(new_output, remaining_letters)


def phone_number_letters(numbers):
    """Parent function for the following problem:

    Given a digit string, return all possible letter combinations that the 
    number could represent.

    Input:Digit string "23"
    Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

    A mapping of digit to letters (just like on the telephone buttons) is given below.
    """
    if len(numbers) == 0:
        return []
    letters = _get_letters(numbers)
    return _get_letter_combis([], letters)


def count_steps(steps):
    """You are climbing a stair case. It takes n steps to reach to the top.
    Each time you can either climb 1 or 2 steps. In how many distinct ways can
    you climb to the top?
    """
    print steps
    if steps == 0:
        print 'Found 1!'
        return 1
    elif steps - 2 >= 0:
        return count_steps(steps - 2) + count_steps(steps - 1)
    else:
        return count_steps(steps - 1)


def get_site_limit_exceeders(T, window=2, frame=3):
    out = []
    adr = []
    for i, t in enumerate(T):
        suspects = []
        for t2 in T[i:]:
            if t2 - t < frame:
                suspects.append(t2)
        try:
            for suspect in range(i + window, len(suspects)):
                if suspect not in adr:
                    adr.append(suspect)
                    out.append(T[suspect])
        except:
            pass
    return out


if __name__ == '__main__':
    print get_site_limit_exceeders([1,1,2,5,6,8])
