import argparse
import sys
from heapq import heappush, heappop
from itertools import count
from datetime import date


class TaxLots:

  index = None
  date_finder = None # look up items in queue by date
  strategy = None # fifo or hifo
  pq = None # priority queue
  REMOVED = -1

  def __init__(self, lots=[], strategy='fifo'):
    self.strategy = strategy
    self.date_finder = {}
    self.pq = []
    self.index = count(start=1)
    self.load_trades(lots)
  
  def __str__(self) -> str:
    # sort by index
    sorted_lots = sorted(self.pq, key=lambda x: x[-1]) 
    lines = [f'{lot[-1]},{lot[1]},{lot[2]:.2f},{lot[3]:.8f}' for lot in sorted_lots if lot[-1] != self.REMOVED]
    return '\n'.join(lines)
  
  def _aggregate_lot_buys(self, lot, trade) -> [date | float, date, float, float, int]:
    total_quantity = lot[3] + trade[2]
    total_cost = lot[2] * lot[3] + trade[1] * trade[2]
    total_price = total_cost / total_quantity
    priority = lot[1] if self.strategy == 'fifo' else -total_price
    return [priority, lot[1], total_price, total_quantity, lot[-1]]


  def buy(self, trade) -> None:
    date, price, amount = trade
    priority = date if self.strategy == 'fifo' else -price

    # new lot
    if date not in self.date_finder:
      lot = [priority, date, price, amount, next(self.index)]
      self.date_finder[date] = lot
      heappush(self.pq, lot)

    # combine with existing lot
    else:
      lot = self.date_finder[date]
      new_lot = self._aggregate_lot_buys(lot, trade)
      lot[-1] = self.REMOVED
      self.date_finder[date] = new_lot
      heappush(self.pq, new_lot)
  
  def sell(self, trade) -> None:
    date, price, total_amount = trade
    while total_amount and len(self.pq):
      priority, date, price, amount, index = heappop(self.pq)
      if index is self.REMOVED:
        continue
      if amount < total_amount:
        total_amount -= amount
        del self.date_finder[date]
      else:
        amount -= total_amount
        del self.date_finder[date]
        priority = date if self.strategy == 'fifo' else -price
        lot = [priority, date, price, amount, index]
        self.date_finder[date] = lot
        heappush(self.pq, lot)
        return
    if total_amount > 0 and len(self.pq) == 0:
      raise Exception('Error: Sell quantity exceeded inventory')


  def parse_trade(self, raw_trade: [str, str, str, str]) -> [date, str, float, float]:
    try:
      return [date.fromisoformat(raw_trade[0]), raw_trade[1], float(raw_trade[2]), float(raw_trade[3])]
    except Exception as e:
      raise Exception(f'Failed to parse trade: {raw_trade}\n({e})')

  def load_trades(self, raw_trades: list[(str, 'buy' or 'sell', str, str)]) -> None:
    trades = [self.parse_trade(raw) for raw in raw_trades]
    for trade in trades:
      if trade[1] == 'buy':
        self.buy([trade[0], trade[2], trade[3]])
      else:
        self.sell([trade[0], trade[2], trade[3]])


def main():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('algorithm', choices=['hifo', 'fifo'], action='store', help='ordering algorithm for selling tax lots')
  args = arg_parser.parse_args()
  lines = []
  try:
    lines = [line.split(',') for line in sys.stdin.read().splitlines()]
  except Exception as e:
    raise Exception('Failed to parse input. Input should contain multiple lines of csv data.\n', e)

  taxlots = TaxLots(lines, args.algorithm)
  print(taxlots)
    
if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print(e)
    print('Exiting...')
    sys.exit(1)
