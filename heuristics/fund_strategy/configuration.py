
from dataclasses import dataclass


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
