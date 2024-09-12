C_FILLED_CELL = "#5a3896"
C_EMPTY_CELL = "#ffffff"

class Cell:
	def __init__(self, grid_position, completion_state):
		self.grid_pos = grid_position
		self.curr_state = 1
		self.comp_state = completion_state
		self.colour = C_EMPTY_CELL

	def change_colour(self):
		if self.curr_state == 1:
			self.colour = C_EMPTY_CELL
		elif self.curr_state == 2:
			self.colour = C_FILLED_CELL
		else:
			self.colour = C_EMPTY_CELL