from datetime import datetime
import time
import utils
import constants

current_unofficial_world_champion = "DrDrunkenstein" # Magnus Carlsen's first real account (?)
last_title_change = utils.lichess_join_date(current_unofficial_world_champion)
games_played_with_title = 0
champion_history = []

min_time = last_title_change
max_time = min_time + constants.week_ms

while last_title_change < utils.datetime_to_utc_ms(datetime.utcnow()):
	prev_unofficial_world_champion = current_unofficial_world_champion

	pgns = utils.get_lichess_pgns(min_time, max_time, current_unofficial_world_champion)
	for pgn in pgns[::-1]: # use reverse of list to search in chronological order (we want first loss)
		games_played_with_title += 1
		tag_dict = utils.parse_pgn(pgn)
		if tag_dict['White'] == current_unofficial_world_champion and tag_dict['Result'] == '0-1':
			save_info = (tag_dict['Black'], tag_dict['White'], tag_dict['UTCDate'], tag_dict['UTCTime'], tag_dict['Site'], str(games_played_with_title))
			current_unofficial_world_champion = tag_dict['Black']
			last_title_change = utils.datetime_to_utc_ms(utils.day_time_to_datetime(tag_dict['UTCDate'], tag_dict['UTCTime']))
			games_played_with_title = 0
			print(save_info)
			with open("worldchamp2.txt", 'a') as f:
				f.write(' '.join(save_info) + '\n')
			break
		elif tag_dict['Black'] == current_unofficial_world_champion and tag_dict['Result'] == '1-0':
			save_info = (tag_dict['White'], tag_dict['Black'], tag_dict['UTCDate'], tag_dict['UTCTime'], tag_dict['Site'], str(games_played_with_title))
			current_unofficial_world_champion = tag_dict['White']
			last_title_change = utils.datetime_to_utc_ms(utils.day_time_to_datetime(tag_dict['UTCDate'], tag_dict['UTCTime']))
			games_played_with_title = 0
			print(save_info)
			with open("worldchamp2.txt", 'a') as f:
				f.write(' '.join(save_info) + '\n')
			break
	if current_unofficial_world_champion == prev_unofficial_world_champion:
		# Defended a whole week! Check next week for a loss...
		min_time += constants.week_ms
		max_time += constants.week_ms
	else:
		# Start looking from previous title change
		min_time = last_title_change + constants.second_ms
		max_time = min_time + constants.week_ms
	time.sleep(constants.self_rate_limit) # Don't overload lichess!