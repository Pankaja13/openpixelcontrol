MAX_LEDS = 500

class Branch:
	def __init__(self, start_led, end_led, children=None):
		if children is None:
			self.children = []
		else:
			self.children = children
		self.parent = None
		self.start_led = start_led
		self.end_led = end_led
		self.led_data = []

		if end_led < start_led:
			raise ValueError()

		for start_led in range(start_led, end_led + 1):
			self.led_data.append((0,0,0))

	def __str__(self):
		return f"<Branch {self.start_led} - {self.end_led}>"

	def print_test(self):
		if self.children:
			for child in self.children:
				child.print_test()
		else:
			print("yo")
			print(self)

		# for index, color_data in enumerate(self.led_data):
		# 	position = index + self.start_led
		# 	print(position, color_data)

branch_a = Branch(101, 150)
branch_b = Branch(151, 200)
branch_c = Branch(201, 250)
branch_d = Branch(251, 300)
branch_e = Branch(301, 350)

main = Branch(0, 100, children=[
	branch_a,
	branch_b,
	branch_c,
	branch_d,
	branch_e,
])

main.print_test()