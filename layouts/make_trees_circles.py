
x_length = 25
x_trees = 5
y_length = 25
y_trees = 5

strip_length = 4.87
leds_per_strip = 300

circle_radius = 0.7751
z_height = 3

###########################################
import math


x_spacing = x_length/x_trees
y_spacing = y_length/y_trees

x_offset = x_spacing/2
y_offset = y_spacing/2

circumference = 2 * math.pi * circle_radius
leds_in_circle = int(circumference * leds_per_strip/strip_length)

print("leds_in_circle", leds_in_circle)

channels = []


def make_circle(x_center, y_center):

	points = []
	for j in range(leds_in_circle):
		theta = j / leds_in_circle * math.pi * 2
		x_cir = math.sin(theta) * circle_radius
		y_cir = math.cos(theta) * circle_radius
		points.append([x_cir + x_center, y_cir + y_center, z_height])

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
		this_channel = make_circle(x_tree_c, y_tree_c)
		channels.append(this_channel)


for index, channel in enumerate(channels):
	write_to_file(f'output/trees_circles_{(index+1):02}', channel)
