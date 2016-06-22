class Choice(object):
    def __init__(self):
        self.name = None
        self.choice = None
        self.priorities = {}
        self.options = []
    
    def get_name(self):
        print 'First, let\'s name the decision you\'re trying to make.'
        self.name = raw_input('> ')

    def get_priorities(self):
        """Prompts user for priorities and their importance from command line,
        then stores as self.priorities for later
        """
        print "Now let\'s get a sense for the criteria you\'ll use to make the call. Type 'q' when you're finished"
        while True:
            print 'Priority name:'
            priority_name = raw_input('> ')
            if priority_name == 'q':
                break
            print "Now rank the importance of %s for your decision on a scale from 1 - 5" % priority_name
            priority_value = int(raw_input('> '))
            if priority_value == 'q':
                break
            self.priorities[priority_name] = priority_value

    def get_options(self):
        """Prompts user for choice options from command line, then stores as 
        self.options for later
        """
        print "Now let's think about how your options stack up."
        print
        more_options = 'y'
        while more_options == 'y':
            option = Option(self.priorities.keys())
            option.get_name()
            option.priority_values()
            self.options.append(option)
            print "Want to enter more options? (y/n)"
            more_options = raw_input('> ')

    def weight_options(self):
        for option in self.options:
            for priority in self.priorities.keys():
                option.option_priorities[priority] *= self.priorities[priority]
                option.score += option.option_priorities[priority]
        self.options = sorted(self.options, key=lambda option: option.score, reverse=True)
        print [(option.option_priorities, option.score) for option in self.options]

    def output_scores(self):
        print "%s decision output" % self.name
        print "==="
        for option in self.options:
            print "option: " + option.name
            print "score:  " + str(option.score)
            print "breakdown:"
            print option.option_priorities
            print


class Option(object):
    def __init__(self, global_priorities):
        self.name = None
        self.global_priorities = global_priorities
        self.option_priorities = {}
        self.score = 0

    def get_name(self):
        """User inputs name of option from command line"""
        print 'Name an option.'
        self.name = raw_input('> ')

    def priority_values(self):
        """ User inputs values of priorities"""
        for priority in self.global_priorities:
            print "How does %s stack up on %s, (scale of 1-5)?" % (self.name, priority)
            option_priority_value = int(raw_input('> '))
            self.option_priorities[priority] = option_priority_value


def main():
    pass
    

if __name__ == '__main__':
    choice = Choice()
    choice.get_name()
    print 'choice name: %s' % choice.name
    choice.get_priorities()
    print 'priorities'
    print choice.priorities
    choice.get_options()
    print choice.options
    choice.output_scores()
