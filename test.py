import unittest
from taxes import TaxLots

class TestTaxLots(unittest.TestCase):

  def test_buy(self):
    lots = TaxLots([], 'fifo')
    lots.buy(('2022-01-01', 100, 1))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,1.00000000')

  def test_aggregate_lot_buys(self):
    lots1 = TaxLots([], 'fifo')
    lot1 = ['2022-01-01', 100, 10]
    lot2 = ['2022-01-01', 100, 20]
    lots1.buy(lot1)
    lots1.buy(lot2)
    self.assertEqual(str(lots1), '1,2022-01-01,100.00,30.00000000')
  
  def test_sell(self):
    lots = TaxLots([], 'fifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.sell(('2022-02-01', 50, 5))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,5.00000000')

  def test_sell_multiple_lots_fifo(self):
    lots = TaxLots([], 'fifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 200, 20))
    lots.sell(('2022-02-01', 50, 5))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,5.00000000\n2,2022-02-01,200.00,20.00000000')

  def test_sell_multiple_lots_hifo(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 200, 20))
    lots.sell(('2022-02-01', 50, 5))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,10.00000000\n2,2022-02-01,200.00,15.00000000')

  def test_big_sell_fifo(self):
    lots = TaxLots([], 'fifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 200, 20))
    lots.sell(('2022-02-01', 200, 25))
    self.assertEqual(str(lots), '2,2022-02-01,200.00,5.00000000')

  def test_big_sell_hifo(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 200, 20))
    lots.sell(('2022-02-01', 200, 25))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,5.00000000')

  def test_bad_date(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 200, 20))
    lots.sell(('2022-02-01', 200, 25))
    self.assertEqual(str(lots), '1,2022-01-01,100.00,5.00000000')

  def test_bad_sell(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 100, 10))
    with self.assertRaises(Exception):
      lots.sell(('2022-02-01', 200, 25))

  def test_bad_sell_2(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 100, 10))
    lots.buy(('2022-02-01', 300, 20))
    lots.buy(('2022-03-01', 400, 30))
    lots.buy(('2022-04-01', 100, 40))
    with self.assertRaises(Exception):
      lots.sell(('2022-02-01', 9000, 101))

  def test_sell_before_buy(self):
    lots = TaxLots([], 'hifo')
    with self.assertRaises(Exception):
      lots.sell(('2022-02-01', 200, 25))
  
  def test_aggregate_buys(self):
    lots = TaxLots([], 'hifo')
    lots.buy(('2022-01-01', 0, 10))
    lots.buy(('2022-01-01', 200, 10))
    lots.buy(('2022-01-01', 400, 40))
    self.assertEqual(str(lots), '1,2022-01-01,300.00,60.00000000')
  
  def test_illigal_price(self):
    lots = TaxLots([], 'hifo')
    with self.assertRaises(Exception):
      lots.parse_trade(['2022-01-01','buy', -1, 1])

  def test_illigal_quantity(self):
    lots = TaxLots([], 'hifo')
    with self.assertRaises(Exception):
      lots.parse_trade(['2022-01-01','buy', 1, 0])

  def test_illigal_action(self):
    lots = TaxLots([], 'hifo')
    with self.assertRaises(Exception):
      lots.parse_trade(['2022-01-01','testy', 1, 1])

  def test_illigal_date(self):
    lots = TaxLots([], 'hifo')
    with self.assertRaises(Exception):
      lots.parse_trade(['testy','buy', 1, 1])

if __name__ == '__main__':
  unittest.main()