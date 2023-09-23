"""
A hill climbing algorithm for solving the best grid strategy.
"""

from datetime import date
from random import random

from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from heuristics.fund_strategy.configuration import Conf
from heuristics.fund_strategy.enums import trade_type

from heuristics.fund_strategy.solution import Solution
from heuristics.accept import AcceptCriterion, HillClimbing
from utils.time import days_between


class OperationRecroder:
    def __init__(self):
        self.history = []

    def record(self, trade):
        self.history.append(trade)

    def draw(self):
        fig, ax = plt.subplots(figsize=(30, 6))

        # 设置x轴的日期格式和刻度
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.set_xlim(min(dates), max(dates))

        ax.plot(dates, prices, color='black', lw=0.5)

        # 在操作节点添加标记
        buy_indices = [i for i, trade in enumerate(
            self.history) if trade == trade_type.BUY]
        sell_indices = [i for i, trade in enumerate(
            self.history) if trade == trade_type.SELL]

        buy_dates = [dates[i] for i in buy_indices]
        buy_prices = [prices[i] for i in buy_indices]
        sell_dates = [dates[i] for i in sell_indices]
        sell_prices = [prices[i] for i in sell_indices]

        ax.scatter(buy_dates, buy_prices, c='g', marker='^', s=20)
        ax.scatter(sell_dates, sell_prices, c='r', marker='v', s=20)

        # 添加轴标签等
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Fund Price History')
        ax.legend(['Price', 'Buy', 'Sell'], loc='best')

        # Automatically adjust the tilt of date labels to prevent overlap
        fig.autofmt_xdate()

        plt.savefig('fund.pdf', format='pdf')


def init():
    """
    init a solution
    """
    return Solution(random(), random())


def should_trade(sol: Solution,  last_price, cur_price):
    """
    decide what kind of trade to do
    """
    if (cur_price - last_price) / last_price >= sol.x2:
        return trade_type.SELL
    elif (last_price - cur_price) / last_price >= sol.x1:
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

    recorder = OperationRecroder()
    recorder.record(trade_type.BUY)

    for i in range(1, len(dates)):
        if days_between(last_date, dates[i]) <= conf.min_trade_interval:
            recorder.record(trade_type.HOLD)
            continue
        action = should_trade(sol, last_price, prices[i])
        if action == trade_type.SELL:
            if cur_shares >= conf.share_per_op:
                cur_shares -= conf.share_per_op
                cur_money += prices[i] * conf.share_per_op
                last_date = dates[i]
                last_price = prices[i]
            else:
                action = trade_type.HOLD
        elif action == trade_type.BUY:
            if cur_money >= prices[i] * conf.share_per_op:
                cur_shares += conf.share_per_op
                cur_money -= prices[i] * conf.share_per_op
                last_date = dates[i]
                last_price = prices[i]
            else:
                action = trade_type.HOLD
        recorder.record(action)

    return cur_money + cur_shares * prices[-1], recorder


def new_solution_from(sol: Solution):
    """
    change the `sol` to generate a new solution
    """
    delta1 = random() * 0.2 - 0.1  # [-0.1, 0.1)
    delta2 = random() * 0.2 - 0.1  # [-0.1, 0.1)
    # make sure in range [0.001, 0.5]
    new_x1 = min(0.2, max(0.001, sol.x1 + delta1))
    new_x2 = min(0.2, max(0.001, sol.x2 + delta2))
    return Solution(new_x1, new_x2)


def search(conf: Conf,
           criterion: AcceptCriterion):
    """
    search algorithm
    """
    # initialization
    cur_sol = init()
    cur_return, cur_history = f(cur_sol, conf)

    best_sol = cur_sol
    best_return, best_history = cur_return, cur_history

    for i in range(conf.max_iters):
        logger.info(
            f"iter {i}: best return: {best_return} | best sol: {best_sol}")
        new_sol = new_solution_from(cur_sol)
        new_return, new_history = f(new_sol, conf)

        if criterion.accept(-cur_return, -new_return):
            cur_sol = new_sol
            cur_return = new_return
            cur_history = new_history

            if cur_return >= best_return:
                best_sol = cur_sol
                best_return = cur_return
                best_history = cur_history
    return best_sol, best_return, best_history


def read_history(filepath: str):
    df = pd.read_csv(filepath)
    dates = list(reversed(df['FSRQ'].to_list()))
    dates = [date.fromisoformat(d) for d in dates]
    prices = list(reversed(df['DWJZ'].to_list()))
    return dates, prices


if __name__ == '__main__':
    logger.remove()
    logger.add("log/hill_climbing.log")
    dates, prices = read_history("data/003579.csv")
    accept_criterion = HillClimbing()
    conf = Conf(1000, 10000, 200, 1000, 7)
    best_sol, best_return, history = search(conf, accept_criterion)
    print(best_sol)
    print(best_return)
    history.draw()
