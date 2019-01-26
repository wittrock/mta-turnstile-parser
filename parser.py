import collections
import datetime
import math
import sys

with open('combined.csv', 'r') as f:
    rows = f.readlines()

combined_entries_per_turnstile = collections.defaultdict(lambda: collections.defaultdict(int))

# not grouping by subway line for now
for row in rows:
    split = row.split(',')
    if len(split) !=  11:
        # only accept the new format of lines (one entry per line, and no plain newlines)
        continue
    
    turnstile_id = '{},{},{}'.format(split[0], split[1], split[2])
    date = split[6]
    time = split[7]
    entries = int(split[9])
    exits = int(split[10])
    
    time_of_reading = datetime.datetime.strptime(date + ' ' + time , '%m/%d/%Y %H:%M:%S')

    # round datetime down to the previous multiple of four hours (0, 4, 8, 12, 16, 20)
    hour = time_of_reading.hour
    rounded_down_hour = hour - (hour%4)
    rounded_time_of_reading = time_of_reading.replace(hour=rounded_down_hour, minute=0, second=0, microsecond=0)

    combined_entries_per_turnstile[turnstile_id][rounded_time_of_reading.isoformat()] = entries

#debug_deltas = {}

MAX_INCONSISTENCY = 1000
MAX_DELTA_PER_BLOCK = 10000
def parse_turnstile(turnstile_id, sorted_entries):
    entries = []
    last_entry = None
    last_entry_time = None
    for timestamp, entry in sorted_entries:
        if last_entry is None:
            # this is the first appearance of a turnstile in the
            # dataset, so set its delta to zero. we lose data for it
            # for this block, but there's no way of rationalizing what
            # it should be.
            delta = 0
        else:
            # normal case.
            delta = entry - last_entry

        if delta < 0:
            # omit drops in entries
            delta = 0
        if delta > MAX_DELTA_PER_BLOCK:
            # drop rises in entries which are clearly bonkers - they
            # admit more than 10,000 people per block.
            delta = 0

        entries.append((timestamp, delta))            
        last_entry = entry
        last_entry_time = timestamp
    return entries            
        
        
 #        if last_entry is not None and entry < last_entry:
 #            inconsistency = last_entry - entry
 #            print('Found drop in turnstile {}, went from {} at {} to {} entries at {}. Drop: {}'.format(turnstile, last_entry, last_entry_time, entry, timestamp, inconsistency))
 #            if inconsistency > MAX_INCONSISTENCY:
 #                return None
 #        if last_entry is not None:
 #            delta = entry - last_entry
 #            if delta > MAX_DELTA_PER_BLOCK:
 #                delta = 0
 #        else:
 #            delta = 0
 #        entries.append((timestamp, delta))
 # #       debug_deltas[turnstile_id + timestamp] = delta
 #        last_entry = entry
 #        last_entry_time = timestamp
#    return entries

# all turnstiles have their entries and exits
parsed_turnstiles = 0
system_wide_deltas = collections.defaultdict(int)
for turnstile, entries in combined_entries_per_turnstile.items():
    sorted_entries = sorted(entries.items(), key=lambda kv: kv[0])
    turnstile_deltas = parse_turnstile(turnstile, sorted_entries)
    if turnstile_deltas is None:
        continue
    parsed_turnstiles += 1
    for timestamp, delta in turnstile_deltas:
        system_wide_deltas[timestamp] += delta
    
print('Parsed {}/{} turnstiles effectively'.format(parsed_turnstiles, len(combined_entries_per_turnstile)))

#debug huge deltas
# sorted_by_deltas = sorted(debug_deltas.items(), key=lambda kv: kv[1], reverse=True)
# deltas_printed = 0
# for pair in sorted_by_deltas:
#     if deltas_printed > 50:
#         break
#     print(pair)
#     deltas_printed += 1

with open('combined_entries.csv', 'w+') as csv_file:
    csv_file.write('block_start,entries_to_whole_system\n')
    sorted_by_time = sorted(system_wide_deltas.items(), key=lambda kv: kv[0])    
    for pair in sorted_by_time:
        csv_file.write(pair[0] + ',' + str(pair[1]) + '\n')


        
