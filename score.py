import sys, time, math
import numpy as np
from collections import defaultdict
from trussme import truss

def fos_score(fos):
	k = 10
	return (math.atan((fos - 1) * 10) / math.pi) + 0.5

def truss_from_X(x):
	t1 = truss.Truss()
	nodes = defaultdict()
	nodes.default_factory = nodes.__len__
	members = set()
	
	for i, j in np.ndindex(x.shape):
		if x[i, j] > 0:
			nodes[(i,j)]
			nodes[(i+1,j)]
			nodes[(i,j+1)]
			nodes[(i+1,j+1)]

			members.add(((i,j),   (i+1, j+1)))
			members.add(((i,j),   (i+1, j)))
			members.add(((i,j),   (i, j+1)))
			members.add(((i+1,j), (i+1, j+1)))
			members.add(((i,j+1), (i+1, j+1)))

	# Add joints
	for ((i,j), n) in sorted(nodes.items(), key = lambda t: t[1]):
		if i == x.shape[0]:
			t1.add_support(np.array([j, x.shape[0] - i, 0.0]), d=2)
		else:
			t1.add_joint(np.array([j, x.shape[0] - i, 0.0]), d=2)

	# Add members
	for m_a, m_b in members:
		t1.add_member(nodes[m_a], nodes[m_b])

	# Add Forces
	x_force = 2500
	y_force = -10000
	
	for i, j in np.ndindex(x.shape):
		# x force
		if x[i, j] == 2:
			t1.joints[nodes[(i,j+1)]].loads[0] = x_force
		# y force
		elif x[i, j] == 3:
			t1.joints[nodes[(i,j)]].loads[1] = y_force

	return t1

def score_and_fos(x):
	t = truss_from_X(x)
	try:
		t.calc_mass()
		t.calc_fos()
	except:
		return [0, 0]

	fos  = t.fos_total
	mass = t.mass

	if mass == 0:
		return [0, fos]

	return [(1 / mass) * fos_score(fos), fos]

def score(x):
	return score_and_fos(x)[0]