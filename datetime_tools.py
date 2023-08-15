'''
Name: datetime_tools.py

What:
Simple tools to manipulate datetime values
'''


import datetime

def day_before(date):
	return date - datetime.timedelta(days=1)


def day_after(date):
	return date + datetime.timedelta(days=1)



def days_between(day1, day2):
	d1 = datetime.datetime.strptime(day1, "%Y-%m-%d")
	d2 = datetime.datetime.strptime(day2, "%Y-%m-%d")
	return abs((d2 - d1).days)


# print(days_between(str(datetime.date(2017,7,31)),str(datetime.date.today())))



def string_to_timedelta(s):
	minutes = int(s.split(':')[0])
	seconds = int(s.split(':')[-1])

	return datetime.timedelta(minutes=minutes, seconds=seconds)


#print(string_to_timedelta('00:21'))



def at_least_timedelta(timedelta, hours=0, minutes=0, seconds=0):
	return timedelta >= datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


#print(at_least_timedelta(string_to_timedelta('02:25'),seconds=30))



def convert_time(offset_hours):
	return datetime.datetime.utcnow() + datetime.timedelta(hours=offset_hours)

# print(convert_time(8))

