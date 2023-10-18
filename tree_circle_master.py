import time

from python.config import trees_config
from python.mode_manager import Modes, Tree
from python.utils import flush_all_pixels
import multiprocessing

if __name__ == '__main__':

	trees_data = []

	for this_tree_config in trees_config:
		trees_data.append(Tree(Modes.JUMP, this_tree_config['host'], this_tree_config['channel']))

	try:
		while True:
			list_start = time.time()
			for number, tree in enumerate(trees_data):
				start = time.time()
				# for each tree
				pixels = tree.get_pixels()
				if pixels:

					tree.send_data(pixels)

				fps = 1 / (time.time() - start)
				print(f"fps: {int(fps)}")
			print(time.time() - list_start)
			time.sleep(0.001)

			# break

	finally:
		# pass
		for tree in trees_data:
			# for _ in range(3):
			flush_all_pixels(tree.send_data)
			# time.sleep(0.1)
