"""Take a combined_entries.csv file and remove all the dates.

Just leave the hour blocks on a graph, with the values the average of
the total entries for that hour over all time.

"""

from collections import defaultdict

import datetime
import iso8601
import sys

entries_by_dow_and_hour = defaultdict(int)

with open(sys.argv[1], 'r') as f:
    line_num = 0
    for line in f.readlines():
        if line_num == 0:
            # remove heading.
            line_num +=1 
            continue
        split = line.split(',')
        ts = iso8601.parse_date(split[0])
        entries = int(int(split[1]) / 158.0) # this is a horrible
                                             # hardcode but tries to
                                             # get at a daily average
                                             # by dividing by the
                                             # number of weeks between
                                             # the start of the data
                                             # (12/1262015)
                                             # and now (1/22/2019)

        # All the entries are defined to be on a four-hour multiple.
        # Extract the day of the week and the hour index on that.
        day_of_week = ts.weekday()
        hour = ts.hour

        entries_by_dow_and_hour[(day_of_week,hour)] += entries
        
        line_num += 1

days_of_week = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}
        
sorted_dow_and_hour = sorted(entries_by_dow_and_hour.items(), key=lambda kv: kv[0])
with open('bucketed_entries.csv', 'w+') as out_file:
    out_file.write('time_bucket,total_all_time_entries\n')
    for time_bucket, entries in sorted_dow_and_hour:
        out_file.write('{}-{},{}\n'.format(days_of_week[time_bucket[0]],time_bucket[1],entries))
    
    
