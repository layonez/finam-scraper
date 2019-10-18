import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'jobs',
            '-a',
            'start_date=2019/01/01',
            '-a',
            'end_date=2019/02/01',
            '-o',
            '2019_01-02.csv',
            '-t',
            'csv'
        ]
    )
except SystemExit:
    pass
