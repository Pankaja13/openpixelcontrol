from math import floor

from python.color_utils import hls_to_rgb_normalized

trunk = [0, 100]
branches = {
	"branchA": [101, 150],
	"branchB": [151, 200],
	"branchC": [201, 250],
	"branchD": [251, 300],
	"branchE": [301, 350],
}

black = (0, 0, 0)

def init():

	def init_pixels(led_range: list):
		return [black for _ in range(led_range[0], led_range[1] + 1)]

	data =  {
		"current_pixels": {
			"trunk": init_pixels(trunk),
			"branches": [
				init_pixels(branches['branchA']),
				init_pixels(branches['branchB']),
				init_pixels(branches['branchC']),
				init_pixels(branches['branchD']),
				init_pixels(branches['branchE']),
			]
		},
		'amplitude': 0,
		'color_index': 0
	}

	return data


def update(data):
	amplitude = data['amplitude']
	base_color = hls_to_rgb_normalized(data['color_index'] / 500, 0.5, 1)
	data['color_index'] += 1
	if data['color_index'] > 500:
		data['color_index'] = 0

	print(base_color)

	new_color = (floor(amplitude * base_color[0]), floor(amplitude * base_color[1]), floor(amplitude * base_color[2]))

	data['current_pixels']['trunk'].insert(0, new_color)
	leaving_trunk = data['current_pixels']['trunk'].pop()
	# print(leaving_trunk)

	pixels = []

	pixels += data['current_pixels']['trunk']

	for branch in data['current_pixels']['branches']:
		branch.insert(0, leaving_trunk)
		branch.pop()

		pixels += branch

	return pixels



if __name__ == "__main__":
	pass
