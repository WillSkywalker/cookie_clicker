"""
Cookie Clicker Simulator
Online Version: http://www.codeskulptor.org/#user39_NYjfMqSROG_32.py
"""

# import simpleplot
from math import ceil
from copy import deepcopy
import random

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total = 0.0
        self._current = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "Produced %.1f, now have %.1f cookies, \n%.1f second passed and %.1f CpS now." % (self._total, self._current, self._time, self._cps)

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies >= self._current:
            return ceil((cookies - self._current) / float(self._cps))
        else:
            return 0.0

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._time += time
            self._current += time * self._cps
            self._total += time * self._cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current >= cost:
            self._current -= cost
            self._cps += additional_cps
            self._history_list.append((self._time, item_name, cost, self._total))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clicker = ClickerState()
    build = build_info.clone()
    while clicker.get_time() <= duration:
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), build)
        if item:
            waittime = clicker.time_until(build.get_cost(item))
            if waittime > (duration - clicker.get_time()):
                break
            clicker.wait(waittime)
            clicker.buy_item(item, build.get_cost(item), build.get_cps(item))
            build.update_item(item)
        else: break

    clicker.wait(duration - clicker.get_time())

    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    lowest = float('inf')
    for item in build_info.build_items():
        if build_info.get_cost(item) < lowest:
            lowest = build_info.get_cost(item)
            cheapest = item
    if lowest > time_left * cps + cookies:
        return None
    else:
        return cheapest

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    highest = None
    expensive = None
    for item in build_info.build_items():
        if time_left * cps + cookies >= build_info.get_cost(item) > highest:
            highest = build_info.get_cost(item)
            expensive = item
    else:
        return expensive

def strategy_random(cookies, cps, history, time_left, build_info):
    return random.choice(build_info.build_items())


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cpvalue = None
    best = None
    for item in build_info.build_items():
        cpvalue_now = (build_info.get_cps(item) * time_left) / build_info.get_cost(item)
        if cpvalue_now > cpvalue:
            cpvalue = cpvalue_now
            best = item

    return best
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Random", SIM_TIME, strategy_random)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

