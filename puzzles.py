from __future__ import division
from random import shuffle
from collections import Counter, defaultdict

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
    """Ask Jason on this one, something to do with the number of visits
    within a certain timeframe 
    """
    print get_site_limit_exceeders([1,1,2,5,6,8])
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


    """Give a list of strings, find the mapping from 1-26 for each string 
    that maximize the value for each string. No distingulish between capital 
    letter and lower case, other characters do not count.
    """
        

def die_hard_3_water_measurer(x, y, z):
    """You are given two jugs with capacities x and y litres. There is an 
    infinite amount of water supply available. You need to determine whether 
    it is possible to measure exactly z litres using these two jugs.

    If z liters of water is measurable, you must have z liters of water 
    contained within one or both buckets by the end.

    https://leetcode.com/problems/water-and-jug-problem/
    https://www.youtube.com/watch?v=BVtQNK_ZUJg

    Input: x = 3, y = 5, z = 4
    Output: True
    
    Input: x = 2, y = 6, z = 5
    Output: False

    Test cases:
    print die_hard_3_water_measurer(5, 3, 4) == True
    print die_hard_3_water_measurer(3, 5, 4) == True
    print die_hard_3_water_measurer(3, 5, 7) == True
    print die_hard_3_water_measurer(3, 4, 2) == True
    print die_hard_3_water_measurer(3, 7, 4) == True
    print die_hard_3_water_measurer(2, 6, 5) == False
    print die_hard_3_water_measurer(2, 6, 3) == False
    """
    # check for obvious edge cases
    if x + y < z:
        return False
    elif x == z or y == z or x + y == z:
        return True
    elif x == y:
        return False
    elif x % 2 == 0 and y % 2 == 0 and z % 2 != 0:
        return False
    # find larger jugs for easy coding
    bj, lj = max(x, y), min(x, y)
    # algorithm part
    multiples = int((bj + lj) / lj + 2)
    for multiple in xrange(multiples):
        if abs(lj * (multiple + 1) - bj) == z:
            return True
    return False


def largest_string_value(str_lst):
    """Takes a list of strings and returns a list of the largest values
    that can be created by individually assigning the letters to a number
    1-26
    """
    out = []
    for string in str_lst:
        out.append(_get_string_value(string))
    return out
    
def _get_string_value(string):
    """Helper function for largest_string_value that extracts the greatest 
    value from a string
    test case:
    print largest_string_value(['pprint', 'abc']) == [26 + 26 + 25 + 24 + 23 + 22, 26 + 25 + 24]

    """

    # gets the counts of each character and returns an ordered list of tuples
    letter_freq = Counter(string)
    letter_freq = letter_freq.most_common(len(letter_freq))
    vals = sorted(range(len(letter_freq) + 1, 27), reverse=True)
    # creates dictionary to map highest values to most frequent characters
    str_val_map = defaultdict()
    for i, letter in enumerate(letter_freq):
        str_val_map[letter[0]] = vals[i]
    str_sum = 0
    # maps the values to the characters
    for letter in string:
        str_sum += str_val_map[letter]
    return str_sum


if __name__ == '__main__':
