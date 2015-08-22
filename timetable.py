from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://timetable.ait.ie/reporting/textspreadsheet;student+set;id;AL_KNETW_7_3%0D%0A?t=student+set+textspreadsheet&days=1-5&=&periods=3-20&=student+set+textspreadsheet&weeks=2&template=student+set+textspreadsheet'

print('Fetching timetable..')
request = urlopen(url)
html = BeautifulSoup(request)

day_codes = ('MO', 'TU', 'WE', 'TH', 'FR')
day_ints = (5, 6, 7, 8, 9)
index = 0
previous_end = 0
doc_start = 'BEGIN:VCALENDAR\n'
doc_end = 'END:VCALENDAR'

ical = open('ait_timetable.ics', 'a')
template = open('event_template.txt', 'r').read()

ical.write(doc_start)

print('Converting to Google Calender file..')
for line in html.find_all('tr'):
    timetable = line.find_all('td')
    try:
        module = timetable[0].string
        start_time = timetable[3].string.replace(':', '')
        end_time = timetable[4].string.replace(':', '')
        room = timetable[7].string

        if module is not None and module != 'Activity':
            if previous_end > int(start_time):
                index += 1

            if len(start_time) == 3:
                start_time = '0' + start_time

            event = template.format(day_ints[index], start_time, end_time, day_codes[index], room, module)
            ical.write(event)
            previous_end = int(end_time)

        else:
            continue

    except:
        continue

ical.write(doc_end)
ical.close()

print('Done.')