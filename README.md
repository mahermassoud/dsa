# DSA Web scraper
This repo scrapes <https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx> to get information about various California District of State Architect (DSA) jobs

## Usage
## Input
Have a file named `app_nums_small.csv` in the same directory as `scrape_all.py`. File should hold desired application numbers with corresponding office IDs in format:
```
04,115070
04,115016
04,115013
04,112016
HQ,112016
```

Note that file numbers MUST have the leading 0. "1" will NOT work, but "01" will.  To make this file, make it in Excel/Numbers and export as CSV, but make sure that you highlight the office IDs, right-click "Format Cells" and select "Text", otherwise, the leading 0s will be dropped and the program will crash.

## Output
Output file will be created in same directory as `scrape_all.py` and be called `projs.csv`
