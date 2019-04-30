
# Limitations: needs long critical section
# assuming no link failures
import time
from collections import deque

class Node:
	
	def __init__(self, node_id, status, hasToken=False, OG=[], IC=[]):
		self.id = node_id
		self.status = status # remainder, waiting, critical
		self.hasToken = hasToken
		self.OG = OG # id of outgoing neighbor
		self.IC = IC # id of incoming neighbor
		self.request_queue = deque()

	def Send(self,m, n): # Mutual Exclusion to Network
		pass

	def Recv(self, m, n=None): # Network to Mutual Exclusion
		if m == 'Request':
			self.request_queue.extend(self.IC)
			if self.hasToken:
				if self.status != 'critical':
					self.handleToken()
			elif len(self.request_queue) == 1:
				self.Send(m, self.OG)
		elif m == 'Token':
			self.hasToken = True
			self.Send('MakeOG', self.OG)
			temp = self.IC
			self.IC = self.OG
			self.OG = temp
			if len(self.request_queue) == 0:
				self.handleToken()
		elif m == 'MakeOG': # 1 -> 2 MakeOG 2.og = 1 ic = 0
			self.Send('AckOG',self)
			temp = self.IC
			self.IC = self.OG
			self.OG = temp
		elif m == 'AckOG': # 2 -> 1 AckOG 1.ic = 2 og = 0
			temp = self.IC
			self.IC = self.OG
			self.OG = temp

	def handleToken(self): 
		p = self.request_queue.pop()
		self.status = 'remainder'
		if p != self.id:
			self.hasToken = False
			self.Send("Token", p)
			if len(self.request_queue) > 0:
				self.Send("Request", p)
		else:
			self.status = 'critical'
			self.EnterCS()

	def ReleaseCS(self): # Application to Mutual Exclusion
		self.status = 'remainder'
		if len(self.request_queue) > 0:
			self.handleToken()

	def EnterCS(self): # Mutual Exclusion to Application
		time.sleep(10)  #emulating CS access
		self.ReleaseCS()
		#time.sleep(20)  #waiting 20 sec before requesting CS again


	def RequestCS(self): # Application to Mutual Exclusion
		self.status = 'waiting'
		self.request_queue.append(self)
		if self.hasToken:
			self.handleToken()
		elif len(self.request_queue) == 1:
			self.Send('Request',self,self.OG)
