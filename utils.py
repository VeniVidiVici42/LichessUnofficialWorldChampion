import requests
import calendar
import time
import constants
from datetime import datetime

def lichess_join_date(player):
	return requests.get("http://lichess.org/api/user/DrDrunkenstein").json()['createdAt']

def datetime_to_utc_ms(dt):
	return calendar.timegm(dt.timetuple()) * 1000

def day_time_to_datetime(day, time):
	return datetime.strptime(day + ' ' + time, '%Y.%m.%d %H:%M:%S')

def get_lichess_pgns(start, end, player):
	api_link = "http://lichess.org/api/games/user/{0}".format(player)
	params = {'moves': False, 'since': start, 'until': end}
	response = requests.get(api_link, params)
	while response.status_code == 429:
		# Lichess wants us to slow down
		print("Received 529, sleeping...")
		time.sleep(lichess_rate_limit)
		response = requests.get(api_link, params)
	# different pgns are separated by double newlines
	# unfortunately this also produces e.g. ' 0-1' as its own pgn, which for some reason is included despite requesting to not have the moves
	# filter those out
	return [pgn for pgn in response.text.split('\n\n') if len(pgn) > constants.min_length] # different pgns separated by double newline

def parse_pgn(pgn):
	tags = [tag for tag in pgn.split('\n') if len(tag) > 0] # clear whitespace
	# Each tag is of the form [String "String"], e.g. [White "DrDrunkenstein"]
	# We can build a dict this way
	pgn_dict = {}
	for tag in tags:
		key, val = tag.split(' ', 1)
		pgn_dict[key[1:]] = val[1:-2]
	return pgn_dict

