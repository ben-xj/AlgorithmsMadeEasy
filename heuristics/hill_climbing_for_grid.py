"""
A hill climbing algorithm for solving the best grid strategy.
"""

from datetime import date
from enum import Enum
from heuristics.accept import AcceptCriterion, HillClimbing
from dataclasses import dataclass
from random import random


from loguru import logger
import pandas as pd


@dataclass
class Solution:
    x1: float  # buy ratio
    x2: float  # sell ratio


@dataclass
class Conf:
    """
    algorithm configurations
    """
    max_iters: int
    principal: float
    share_per_op: int
    start_shares: int
    min_trade_interval: int


class trade_type(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


def init():
    """
    init a solution
    """
    return Solution(random(), random())


def days_between(start_date, end_date):
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    delta = end_date - start_date
    return delta.days


def should_trade(sol: Solution,  last_price, cur_price):
    """
    decide what kind of trade to do
    """
    if (cur_price - last_price) / last_price >= sol.x2:
        return trade_type.SELL
    elif (last_price - cur_price) / last_price <= sol.x1:
        return trade_type.BUY
    return trade_type.HOLD


def f(sol: Solution, conf: Conf):
    """
    calculate the return of a solution `sol`
    """
    last_price = prices[0]
    last_date = dates[0]

    cur_shares = conf.start_shares
    cur_money = conf.principal - cur_shares * last_price

    for i in range(conf.min_trade_interval, len(dates)):
        if days_between(last_date, dates[i]) <= conf.min_trade_interval:
            continue
        action = should_trade(sol, last_price, prices[i])
        if action == trade_type.SELL:
            if cur_shares >= conf.share_per_op:
                cur_shares -= conf.share_per_op
                cur_money += prices[i] * conf.share_per_op
                last_date = dates[i]
                last_price = prices[i]
        elif action == trade_type.BUY:
            if cur_money >= prices[i] * conf.share_per_op:
                cur_shares += conf.share_per_op
                cur_money -= prices[i] * conf.share_per_op
                last_date = dates[i]
                last_price = prices[i]

    return cur_money + cur_shares * prices[-1]


def new_solution_from(sol: Solution):
    """
    change the `sol` to generate a new solution
    """
    delta1 = random() * 0.2 - 0.1  # [-0.1, 0.1)
    delta2 = random() * 0.2 - 0.1  # [-0.1, 0.1)
    # make sure in range [0.001, 0.5]
    new_x1 = min(0.5, max(0.001, sol.x1 + delta1))
    new_x2 = min(0.5, max(0.001, sol.x2 + delta2))
    return Solution(new_x1, new_x2)


def search(conf: Conf, criterion: AcceptCriterion):
    """
    search algorithm
    """
    # initialization
    cur_sol = init()
    cur_return = f(cur_sol, conf)

    best_sol = cur_sol
    best_return = cur_return

    for i in range(conf.max_iters):
        logger.info(
            f"iter {i}: best return: {best_return} | best sol: {best_sol}")
        new_sol = new_solution_from(cur_sol)
        new_return = f(new_sol, conf)

        if criterion.accept(-cur_return, -new_return):
            cur_sol = new_sol
            cur_return = new_return

            if cur_return >= best_return:
                best_sol = cur_sol
                best_return = cur_return
    return best_sol, best_return


def read_history(filepath: str):
    df = pd.read_csv(filepath)
    dates = list(reversed(df['FSRQ'].to_list()))
    prices = list(reversed(df['DWJZ'].to_list()))
    return dates, prices


if __name__ == '__main__':
    logger.remove()
    logger.add("log/hill_climbing.log")
    dates, prices = read_history("data/003579.csv")
    accept_criterion = HillClimbing()
    conf = Conf(10, 10000, 200, 1000, 7)
    best_sol, best_return = search(conf, accept_criterion)
    print(best_sol)
    print(best_return)
