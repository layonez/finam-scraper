# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from datetime import timedelta, date
from re import compile
import json
import csv
import urllib.parse
import logging
import sys
import io

# create logger with 'spam_application'
logger = logging.getLogger('spider')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spider.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class JobsSpider(Spider):
    def __init__(self, start_date, end_date, *args, **kwargs):
        super(JobsSpider, self).__init__(*args, **kwargs)

        # extract date part of url
        p = compile('\\d{4}\\/\\d{2}\\/\\d{2}')
        if p.search(start_date) is None or p.search(end_date) is None:
            raise ValueError(
                'Required params start_date and end_date should be in format yyyy/MM/dd\n' +
                'your input was start_date={} end_date={}'.format(start_date, end_date))

        self.counter = 0
        self.start_date = start_date
        self.end_date = end_date
        self.lg = logging.getLogger()

        with io.open('./filteredInstruments.json', 'r', encoding="utf-8") as em_file:
            data = em_file.read()
            self.instruments = json.loads(data)

    handle_httpstatus_list = [403]
    name = 'jobs'
    allowed_domains = ['finam.ru']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ['market',
                               'code',
                               'name',
                               'decp',
                               'child',
                               'id',
                               'per',
                               'datetime',
                               'open',
                               'high',
                               'low',
                               'close',
                               'vol'],
    }

    def start_requests(self):
        st_year, st_month, st_day = int(self.start_date[0:4]), int(
            self.start_date[5:7]), int(self.start_date[8:10])
        end_year, end_month, end_day = int(self.end_date[0:4]), int(
            self.end_date[5:7]), int(self.end_date[8:10])

        start_date = date(st_year, st_month, st_day)
        end_date = date(end_year, end_month, end_day)

        df = '%02d' % start_date.day
        mf = int('%02d' % start_date.month)
        yf = '%04d' % start_date.year

        dt = '%02d' % end_date.day
        mt = int('%02d' % end_date.month)
        yt = '%04d' % end_date.year

        for instrument in self.instruments:
            params = [
                ('market', instrument['market']),
                ('em', instrument['id']),
                ('code', instrument['code']),
                ('apply', '0'),
                ('df', df), # df, mf, yf, from, dt, mt, yt, to – это параметры времени.
                ('mf', mf - 1),
                ('yf', yf),
                ('from', start_date.isoformat().replace('-', '.')),
                ('dt', dt),
                ('mt', mt - 1),
                ('yt', yt),
                ('to', end_date.isoformat().replace('-', '.')),
                ('p', '2'), # p — период котировок (тики, 1 мин., 5 мин., 10 мин., 15 мин., 30 мин., 1 час, 1 день, 1 неделя, 1 месяц)
                ('f', instrument['code'] + '_' + start_date.isoformat()),
                ('e', '.csv'), # e – расширение получаемого файла; возможны варианты — .txt либо .csv
                ('cn', instrument['code']),
                ('dtf', '1'), # dtf — формат даты (1 — ггггммдд, 2 — ггммдд, 3 — ддммгг, 4 — дд/мм/гг, 5 — мм/дд/гг)
                ('tmf', '1'), # tmf — формат времени (1 — ччммсс, 2 — ччмм, 3 — чч: мм: сс, 4 — чч: мм)
                ('MSOR', '0'), # MSOR — выдавать время (0 — начала свечи, 1 — окончания свечи)
                ('mstime', 'on'),
                ('mstimever', '1'), # mstimever — выдавать время (НЕ московское — mstimever=0; московское — mstime='on', mstimever='1')
                ('sep', '1'), # sep — параметр разделитель полей (1 — запятая (,), 2 — точка (.), 3 — точка с запятой (;), 4 — табуляция (»), 5 — пробел ( ))
                ('sep2', '1'), # sep2 — параметр разделитель разрядов (1 — нет, 2 — точка (.), 3 — запятая (,), 4 — пробел ( ), 5 — кавычка ('))
                ('datf', '1'), # datf — Перечень получаемых данных (#1 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #2 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE; #3 — TICKER, PER, DATE, TIME, CLOSE, VOL; #4 — TICKER, PER, DATE, TIME, CLOSE; #5 — DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #6 — DATE, TIME, LAST, VOL, ID, OPER).
                ('at', '1'), # at — добавлять заголовок в файл (0 — нет, 1 — да)
                # ('fsp', '1'), #- заполнять периоды без сделок
            ]
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36',
                'Cookie': 'subscribeModal=cancelled; ASPSESSIONIDCCSCASDA=EHHEGMPBIMAIAPBBDFBMAOAB; ASPSESSIONIDCATDATDA=LLGAEIMCCJNLCNOKPKPFMBJM',
                'Host': 'export.finam.ru'}

            yield Request("http://export.finam.ru/" + instrument['code'] + start_date.isoformat() + ".csv?" + urllib.parse.urlencode(params),
                          headers=headers,
                          meta={'market': instrument['market'],
                                'code': instrument['code'],
                                'name': instrument['name'],
                                'decp': instrument.get('decp', None),
                                'child': instrument['child'],
                                'id': instrument['id'], })

    def parse(self, response):
        self.counter = self.counter + 1
        logger.debug("{0} {1}".format(self.counter, response.meta['code']))

        if response.status == 403:
            logger.error('403: ' + response.url + ' : ' +  str(response.status))
            return

        if response.body == '':
            logger.error('Empty body:' + response.url + ' : ' +
                         str(response.status))
            return
        try:
            reader = csv.reader(response.body.decode("utf-8").split('\r\n'), delimiter=',')
            for row in reader:
                if len(row) == 9 and row[0] != '<TICKER>':
                    yield{'market': response.meta['market'],
                          'code': response.meta['code'],
                          'name': response.meta['name'],
                          'decp': response.meta['decp'],
                          'child': response.meta['child'],
                          'id': response.meta['id'],
                          'per': row[1],
                          'datetime': row[2] + row[3],
                          'open': row[4],
                          'high': row[5],
                          'low': row[6],
                          'close': row[7],
                          'vol': row[8],
                          }

        except:
            logger.error("Parse error: {0}".format(sys.exc_info()))
        finally:
            pass
