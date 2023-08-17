# Tax Lot Selection Task


## Requirements
* Create an executable script which takes one argument and handles input from stdin
* Process an ordered transaction log read from stdin in the format of date,buy/sell,price,quantity separated by line breaks
* The argument passed into the script determines the tax lot selection algorithm
  * fifo - the first lots bought are the first lots sold
  * hifo - the first lots sold are the lots with the highest price
* Keep track of lots internally by an incrementing integer id starting at 1
  * Buys on the same date should be aggregated into a single lot, the price is the weighted average price, the id should remain the same
* Print to stdout the remaining lots after the transaction log is processed in the format of id,date,price,quantity
  * price should have two decimal places
  * quantity should have eight decimal places
* If an error is encountered, print to stdout a descriptive error message and exit the script with a non-zero exit code
* Write automated tests covering all cases the script should handle
* Include instructions on how to build the executable script and run the automated tests

