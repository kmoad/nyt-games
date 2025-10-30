from pathlib import Path



if __name__ == '__main__':
	from argparse import ArgumentParser

	word_list_dir = Path('lists')

	parser = ArgumentParser()
	parser.add_argument('center')
	parser.add_argument('periphery')
	parser.add_argument('--words',
		type = Path,
		default = word_list_dir/'easy.txt',
		help = 'File containing words',
	)
	parser.add_argument('--show',
		type = int,
		default = 10,
		help = 'Number of valid words to show'
	)
	args = parser.parse_args()

	words = [_.strip().upper() for _ in args.words.open()]
	words.sort()

	key_letter = args.center.upper()
	letters = set(args.periphery.upper()+key_letter)

	valid = []
	for word in words:
		if len(word) >= 4 and key_letter in word and set(word).issubset(letters):
			valid.append(word)
	valid.sort(key=lambda _: len(_), reverse=True)
	for word in valid[:args.show]:
		print(word)	