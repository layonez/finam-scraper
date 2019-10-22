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


Also you can edit query settings in `jobs.py`

```python
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
('datf', '1'), # datf — Перечень получаемых данных (#1 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #2 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE; #3 — TICKER, PER, DATE, TIME, CLOSE, VOL; #4  TICKER, PER, DATE, TIME, CLOSE; #5 — DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #6 — DATE, TIME, LAST, VOL, ID, OPER).
('at', '1'), # at — добавлять заголовок в файл (0 — нет, 1 — да)
# ('fsp', '1'), - заполнять периоды без сделок