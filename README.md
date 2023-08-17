# Tax Lot Selection Task

This tool automates tax lot selection based on a provided algorithm. It utilizes a priority queue to efficiently rank and select lots to be sold.
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

## Install
* Requires [Python3](https://www.python.org/downloads/) to be installed

* Clone the repo and install dependencies within a virtual environment  
```shell
git clone git@github.com:alexlwn123/tax-lots.git
cd tax-lots
```
* Opitonal - Activate a virtual environment (MacOS instructions)
```shell
python3 -m pip install venv
python3 -m venv env
source evn/bin/activate
```
* Install dependencies
```shell
pip install -r requirements.txt
```
## Usage

* Run the script
```shell
echo 'echo -e '2021-01-01,buy,10000.00,1.00000000\n2021-02-01,sell,20000.00,0.50000000' | python taxes.py fifo
```
* Help menu
```shell
python taxes.py -h
```

## Testing 

* Run the tests
```shell
python test.py -v
```
## Build & Run as Executable

* Build as an executable
```shell
pyinstaller --onefile taxes.py
```
* Run the executable
```shell
cd dist
echo -e '2021-01-01,buy,10000.00,1.00000000\n2021-02-01,sell,20000.00,0.50000000' | taxes fifo
```


# Production Considerations / Next Steps
If this was going to production, what else should be considered? 
  * Logging
    * Implement detailed logs of calculations and all financial transactions for auditing 
  * Testing
    * Add edge cases to verify accuracy of float math
    * Add cases with large inputs to test performance
    * Add e2e tests with large data streams to test performance
    * Add tests to verify accuracy of intermediate states within logs
  * Documentation
    * Provide additional examples 
    * Provide instructions for more environments
  * Additional Features
    * Additional selection algorithms
    * Refactor code to make it easier to add additional algorithms
    * Options for lot batching (other than each day)
    * Additional formats for input/output (csv, json, xml, etc.) 
    * Interactive prompts to improve the experience of the CLI
    * Pretty print, table view
    * Simple UI for converting files
    * Issolate the business logic from the CLI tool
      * Create a library containing only the calculation engine
    * Cache intermediate states to help recover progress in case of partial failure
    * Multiple currency support
    * Tax calculations