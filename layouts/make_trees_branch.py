from random import randint

x_length = 25
x_trees = 5
y_length = 25
y_trees = 5

strip_length = 4.87
leds_per_strip = 300

number_of_branches = 4
branch_length = strip_length / number_of_branches
h_variance_angle = 90

v_angle_range = [20, 80]
z_height = 2

offset_from_middle = 0.5

filename = "trees_branch"


###########################################
import math


x_spacing = x_length/x_trees
y_spacing = y_length/y_trees

x_offset = x_spacing/2
y_offset = y_spacing/2

led_spacing = 4.87 / 300
leds_per_branch = int(branch_length * leds_per_strip/strip_length)

print("leds_per_branch:", leds_per_branch)


channels = []


def make_branches(x_center, y_center):

	points = []

	for branch_no in range(number_of_branches):
		var_theta = randint(-int(h_variance_angle/2), int(h_variance_angle/2)) / 360 * math.pi * 2
		theta_h = (math.pi * 2 / number_of_branches * branch_no) + var_theta
		theta_v = (math.pi * 2 * randint(v_angle_range[0], v_angle_range[1]) / 360)

		for branch_pix_no in range(leds_per_branch):
			x = math.sin(theta_h) * (((branch_pix_no + 1) * led_spacing) + offset_from_middle)
			y = math.cos(theta_h) * (((branch_pix_no + 1) * led_spacing) + offset_from_middle)
			z = math.sin(theta_v) * (((branch_pix_no + 1) * led_spacing) + offset_from_middle)
			points.append([x + x_center, y + y_center, z + z_height])

	return points


def make_json_line(coordinate):
	return '{"point": [%.2f, %.2f, %.2f]}' % (coordinate[0], coordinate[1], coordinate[2])


def write_to_file(filename, channel_data):
	string = "[\n"
	lines = [make_json_line(coordinate) for coordinate in channel_data]
	string += ',\n'.join(lines) + '\n]'

	with open(f"{filename}.json", "w") as f:
		f.write(string)


for y_tree in range(0, y_trees):
	y_tree_c = (y_tree * y_spacing) + y_offset - (y_length/2)
	for x_tree in range(0, x_trees):
		x_tree_c = (x_tree * x_spacing) + x_offset - (x_length/2)
		this_channel = make_branches(x_tree_c, y_tree_c)
		channels.append(this_channel)


for index, channel in enumerate(channels):
	write_to_file(f'output/{filename}_{index+1}', channel)
