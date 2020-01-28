import pygame
import random
import numpy as np

class automata:

	def __init__(self, size):
		self.boardsize = size
		self.gridsize = 3
		self.state = 0
		self.blocksize = 1
		self.start_x = 200
		self.start_y = 100
		self.scale = 1
		self.board_0 = np.full((self.boardsize*self.boardsize),0, dtype=int)
		random.seed()
		for i in range(0, self.boardsize*self.boardsize):
			self.board_0[i] = random.randint(0, 1)
		self.board_0 = self.board_0.reshape(self.boardsize,self.boardsize)
		self.board_1 = np.full((self.boardsize, self.boardsize), 0, dtype=int)
		self.boards = [self.board_0, self.board_1]


	def reset_board(self, state):
		self.boards[state] = np.full((self.boardsize,self.boardsize),0,dtype=int)


	def apply_rule(self, state, cell_state, board_row, board_column):
		number_of_ON_cells = 0
		for outer_row in range (board_row-1, board_row+2):
			for outer_column in range(board_column - 1, board_column + 2):
				if(outer_row == board_row and outer_column == board_column):
					pass
				else:
					number_of_ON_cells += self.boards[state][outer_row][outer_column]
		if cell_state == 1 and number_of_ON_cells < 2:
			cell_state = 0
		if cell_state == 1 and number_of_ON_cells >= 2 and number_of_ON_cells <= 3:
			cell_state = 1
		if cell_state == 1 and number_of_ON_cells > 3:
			cell_state = 0
		if cell_state == 0 and number_of_ON_cells == 3:
			cell_state = 1
		return cell_state


	def determine_central_cell_state(self, old_state):
		new_state = old_state
		new_state ^= 1
		self.reset_board(new_state)
		for central_row in range(1,self.boardsize-1):
			for central_column in range(1, self.boardsize-1):
				cell_state = self.boards[old_state][central_row][central_column]
				self.boards[new_state][central_row][central_column] = self.apply_rule(old_state, cell_state, central_row, central_column)

	def draw_board(self, current_state, screen):
		background = (40,40,128)
		foreground = (255,255,255)
		previous_state = current_state
		previous_state ^= 1
		for outer_row in range(0, self.boardsize):
			for outer_column in range(0, self.boardsize):
				if outer_row >= 0 and outer_row <= self.boardsize-1 and outer_column >= 0 and outer_column <= self.boardsize-1:
					if self.boards[current_state][outer_row][outer_column] == 0:
						block_colour = background
					else:
						block_colour = foreground
				else:
					block_colour = background
				pygame.draw.rect(screen, block_colour, pygame.Rect(self.start_x+outer_column*self.blocksize*self.scale, self.start_y+outer_row*self.blocksize*self.scale, self.blocksize*self.scale, self.blocksize*self.scale))


state = 0
grid = automata(100)
grid.determine_central_cell_state(state)
pygame.init()
screen = pygame.display.set_mode((900,900))
done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			state ^= 1
			grid.determine_central_cell_state(state)
	grid.draw_board(state, screen)
	pygame.display.flip()
exit()



