import pygame as pg
import random
import sys, os

from Cell import *

os.system("cls" if os.name=="nt" else "clear")
print("Nonograms | Ben Collingridge")

C_BACKGROUND = "#343742"
C_GRID_BOUNDARIES = "#72778c"
C_CROSS_CELL = "#b52450"

GRID_SIZE = pg.Vector2(10, 10)
CELL_SIZE = 60
GRID_PADDING = 100
WIDTH = (CELL_SIZE * GRID_SIZE.x) + (2 * GRID_PADDING)
HEIGHT = (CELL_SIZE * GRID_SIZE.y) + (2 * GRID_PADDING)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Nonograms | Ben Collingridge")

print(f"---------------\n  Window Size\n---------------\nX: {screen.get_width()}, Y: {screen.get_height()}")

cells = []
x_solutions = []
y_solutions = []

def get_cell_clicked(pos):
	for cell in cells:
		cell_start = pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING, cell.grid_pos.y * CELL_SIZE + GRID_PADDING)
		cell_end = pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING + CELL_SIZE, cell.grid_pos.y * CELL_SIZE + GRID_PADDING + CELL_SIZE)
		if pos[0] >= cell_start.x and pos[0] < cell_end.x and pos[1] >= cell_start.y and pos[1] < cell_end.y:
			return cell

def setup():
	# creating and assigning cells to grid
	for i in range(int(GRID_SIZE.x)):
		for j in range(int(GRID_SIZE.y)):
			rng = random.randint(1, 2)
			completion_state = None
			# 1 = empty, 2 = filled, 3 = cross
			if rng == 1:
				completion_state = 3
			else:
				completion_state = 2
			cell = Cell(pg.Vector2(j, i), completion_state)
			cells.append(cell)

	# counting rows
	for y in range(int(GRID_SIZE.y)):
		temp = []
		count = 0
		for x in range(int(GRID_SIZE.x)):
			if cells[y * int(GRID_SIZE.y) + x].comp_state == 2:
				count += 1
				if x == int(GRID_SIZE.y) - 1 and count > 0:
					temp.append(str(count))
			elif cells[y * int(GRID_SIZE.y) + x].comp_state == 3 and count > 0:
				temp.append(str(count))
				count = 0
		x_solutions.append(temp)

	# counting columns
	for x in range(int(GRID_SIZE.x)):
		temp = []
		count = 0
		for y in range(int(GRID_SIZE.y)):
			if cells[y * int(GRID_SIZE.y) + x].comp_state == 2:
				count += 1
				if y == int(GRID_SIZE.y) - 1 and count > 0:
					temp.append(str(count))
			elif cells[y * int(GRID_SIZE.y) + x].comp_state == 3 and count > 0:
				temp.append(str(count))
				count = 0
		y_solutions.append(temp)

	target_filled = 0
	for cell in cells:
		if cell.comp_state == 2:
			target_filled += 1

	game_loop(True, target_filled)

def win_screen(running):
	clock = pg.time.Clock()
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

		screen.fill(C_BACKGROUND)

		font = pg.font.Font("freesansbold.ttf", 34)
		text = font.render(f"You win!", True, "white")
		text_rect = text.get_rect()
		text_rect.center = (screen.get_width() / 2, screen.get_height() / 2 - text_rect.h / 2)
		screen.blit(text, text_rect)

		# RENDER/UPDATE
		pg.display.update()
		pg.display.flip()
		clock.tick(144)

def game_loop(running, tf):
	target_filled = tf
	clock = pg.time.Clock()
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				# check left mouse button is pressed
				if event.button == 1:
					pos = pg.mouse.get_pos()
					cell = get_cell_clicked(pos)
					if cell.curr_state == 1:
						cell.curr_state = 2
					elif cell.curr_state == 2:
						cell.curr_state = 3
					elif cell.curr_state == 3:
						cell.curr_state = 1
					cell.change_colour()

		screen.fill(C_BACKGROUND)

		# draw cells row-by-row
		for cell in cells:
			pg.draw.rect(screen, cell.colour, pg.Rect(pg.Rect(pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING, cell.grid_pos.y * CELL_SIZE + GRID_PADDING), pg.Vector2(CELL_SIZE, CELL_SIZE))))
			if cell.curr_state == 3:
				cell_padding = CELL_SIZE * 0.25
				# draw cross
				# top left to bottom right
				pg.draw.line(screen, C_CROSS_CELL, pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING + cell_padding, cell.grid_pos.y * CELL_SIZE + GRID_PADDING + cell_padding), pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING + CELL_SIZE - cell_padding, cell.grid_pos.y * CELL_SIZE + GRID_PADDING + CELL_SIZE - cell_padding), 4)
				# top right to bottom left
				pg.draw.line(screen, C_CROSS_CELL, pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING + CELL_SIZE - cell_padding, cell.grid_pos.y * CELL_SIZE + GRID_PADDING + cell_padding), pg.Vector2(cell.grid_pos.x * CELL_SIZE + GRID_PADDING + cell_padding, cell.grid_pos.y * CELL_SIZE + GRID_PADDING + CELL_SIZE - cell_padding), 4)

		# draw numbers
		for x in range(len(x_solutions)):
			temp_string = " ".join(x_solutions[x])
			font = pg.font.Font("freesansbold.ttf", 18)
			text = font.render(f"{temp_string}", True, "white")
			text_rect = text.get_rect()
			text_rect.topleft = (GRID_PADDING * 0.1, GRID_PADDING + x * CELL_SIZE + (CELL_SIZE / 2) - (text_rect.h / 2))
			screen.blit(text, text_rect)
		for y in range(len(y_solutions)):
			spacing = 0
			for target in y_solutions[y]:
				font = pg.font.Font("freesansbold.ttf", 18)
				text = font.render(f"{target}", True, "white")
				text_rect = text.get_rect()
				text_rect.center = (GRID_PADDING + y * CELL_SIZE + (CELL_SIZE / 2) - (text_rect.w / 2), GRID_PADDING * 0.15 + spacing)
				screen.blit(text, text_rect)
				spacing += GRID_PADDING / 5

		# draw grid overlay
		for i in range(int(GRID_SIZE.x) + 1):
			if i % 5 == 0:
				pg.draw.line(screen, C_GRID_BOUNDARIES, pg.Vector2(CELL_SIZE * i + GRID_PADDING, GRID_PADDING), pg.Vector2(CELL_SIZE * i + GRID_PADDING, screen.get_height() - GRID_PADDING), 5)
			else:
				pg.draw.line(screen, C_GRID_BOUNDARIES, pg.Vector2(CELL_SIZE * i + GRID_PADDING, GRID_PADDING), pg.Vector2(CELL_SIZE * i + GRID_PADDING, screen.get_height() - GRID_PADDING))
		for j in range(int(GRID_SIZE.y) + 1):
			if j % 5 == 0:
				pg.draw.line(screen, C_GRID_BOUNDARIES, pg.Vector2(GRID_PADDING, CELL_SIZE * j + GRID_PADDING), pg.Vector2(screen.get_width() - GRID_PADDING, CELL_SIZE * j + GRID_PADDING), 5)
			else:
				pg.draw.line(screen, C_GRID_BOUNDARIES, pg.Vector2(GRID_PADDING, CELL_SIZE * j + GRID_PADDING), pg.Vector2(screen.get_width() - GRID_PADDING, CELL_SIZE * j + GRID_PADDING))

		# check win
		target_check = 0
		for cell in cells:
			if cell.comp_state == 2 and cell.curr_state == 2:
				target_check += 1
		if target_check == target_filled:
			win_screen(True)
			running = False

		# RENDER/UPDATE
		pg.display.update()
		pg.display.flip()
		clock.tick(144)

	pg.quit()

setup()