# finam-scraper
Mass quotes export from finam web site

## Requirements
python v2.7, Scrapy 1.7

## How to use
We scrap minute data for all instruments in filteredInstruments.json 
If you decide that instruments list is outdated, than go to finam.ru to get updated list:


Run `runner.py`

OR

In project directory run:

```sh
$ scrapy crawl jobs -a start_date="2019/01/01" -a end_date="2019/02/01" -o 2019_01-02.csv -t csv