import time

from python.config import trees_config
from python.mode_manager import Modes, Tree
from python.utils import flush_all_pixels

if __name__ == '__main__':

	trees_data = []

	for this_tree_config in trees_config:
		trees_data.append(Tree(Modes.RAIN, this_tree_config['host'], this_tree_config['channel']))

	try:
		while True:
			for number, tree in enumerate(trees_data):
				# for each tree
				pixels = tree.get_pixels()
				if pixels:
					# print(number)
					tree.send_data(pixels)
			# break

	finally:
		# pass
		for tree in trees_data:
			for _ in range(3):
				flush_all_pixels(tree.send_data)
				time.sleep(0.1)
