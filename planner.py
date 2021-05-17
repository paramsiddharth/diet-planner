# Diet Planner
import json
import random
import sys
import os
import signal
from pyfiglet import Figlet

signal.signal(signal.SIGINT, lambda *args: None)

def main():
	info_file = os.path.join(os.getcwd(), 'info.json')
	info = None
	try:
		with open(info_file, 'r', encoding='utf-8') as f:
			info = json.load(f)
	except:
		info = {}
		with open(info_file, 'w+', encoding='utf-8') as f:
			json.dump(info, f)

	print(Figlet(font='graffiti').renderText('Diet Planner'))

	print('1. Make entry')
	print('2. Get suggestion')
	x = input('\n> ')

	if x == '1':
		food_item = input('What did you eat? : ')
		x = input(f'You ate {food_item}. [Y/n]: ')
		if x.strip().lower() == 'y' or len(x.strip()) < 1:
			info[food_item] = info.get(food_item, 0) + 1.0

			# Neutralize scores
			min_val = min((info.items()), key=lambda v: v[1])[1]
			for key in info:
				info[key] -= min_val

			with open(info_file, 'w+', encoding='utf-8') as f:
				json.dump(info, f)
			print('Entry added!')
		else:
			print('Entry rejected!')
	elif x == '2':
		if len(info.keys()) < 3:
			print('Not sufficient data. Check back later!')
			sys.exit()
		print('Analyzing diet...')

		min_val = min((info.items()), key=lambda v: v[1])[1]
		choices = list(filter(lambda k: info[k] == min_val, info.keys()))
		choice_count = len(choices)
		choice = choices[random.randint(0, choice_count - 1)]
		info[choice] += 1
		print(f'Today\'s suggestion for you is: {choice}')

		# Neutralize scores
		min_val = min((info.items()), key=lambda v: v[1])[1]
		for key in info:
			info[key] -= min_val
		with open(info_file, 'w+', encoding='utf-8') as f:
			json.dump(info, f)
		print('Enjoy a healthy life!')
	else:
		print('Invalid choice!', file=sys.stderr)
		sys.exit(1)

if __name__ == '__main__':
	try:
		main()
	except EOFError:
		...