from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
import numpy as np
import matplotlib.pyplot as plt

class DiseaseModel(Model):
	"""A model with some number of agents."""
	def __init__(self, N, width, height):
		self.num_agents = N
		self.grid = SingleGrid(width, height, True)
		self.schedule = RandomActivation(self)
		# Create agents
		for i in range(self.num_agents):
			a = DiseaseAgent(i, self)
			self.schedule.add(a)
			# Add the agent to a random grid cell
			location = self.grid.find_empty()
			self.grid.place_agent(a, location)



	def step(self):
		self.schedule.step()

class DiseaseAgent(Agent):
	""" An agent with fixed initial wealth."""
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)
		self.disease = self.random.randrange(2)
		print(self.disease)

	def move(self):
		possible_steps = self.model.grid.get_neighborhood(
			self.pos,
			moore=False,
			include_center=True)
		choice = self.random.choice(possible_steps)
		if model.grid.is_cell_empty(choice):
			self.model.grid.move_agent(self, choice)


	def spread_disease(self):
		cellmates = self.model.grid.get_neighbors(self.pos,moore=False)
		if len(cellmates) > 1:
			other = self.random.choice(cellmates)
			other.disease = 1

	def step(self):
		self.move()
		if self.disease == 1:
			self.spread_disease()



model = DiseaseModel(50, 10, 10)
for i in range(1):
	model.step()


agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
	agent, x, y = cell
	if agent != None:
		print(agent.disease)
		agent_counts[x][y] = agent.disease
	else:
		agent_counts[x][y] = -1
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()
plt.show()
