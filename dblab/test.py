import pymysql
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths

class Tests:

	def make_graph(self):

		con = pymysql.connect(host='localhost', user='root', password='1', db='drive2', charset='utf8')


		curs = con.cursor()
		
		graph = Graph()
		nodeid_sql = "select nodeid from drive2.c1_node"
		cost_sql = "select tonode, length, format(speed,0) from drive2.a3_link_view where fromnode = "

		curs.execute(nodeid_sql)

		rows= curs.fetchall()
		for i in rows:
			nodeid= list(map(lambda x:x,i))
			curs.execute(cost_sql+"'" +nodeid[0]+"';")
			rows=curs.fetchall()

			if rows is None:
				continue
			else:
				for items in list(rows):
					try:
						cost = items[1]/int(items[2])
					except ZeroDivisionError:
						cost = 0
					graph.add_edge(i[0], items[0], cost)

		con.close()
		return graph

	def find_short_path(self,pgraph,s,d,node_list):
		path =[]
		node=[]
		min_cost = 10	
		count = 0
		path_count=0
		print(node_list)
		for i in range(3):
			small_node=[]
			for j in range(2):
				small_node.append(node_list[count])
				count+=1
			node.append(small_node)
		print(node)
		for j in range(6):
			for i in range(3):
					if not node[i]:
						continue
					print('check node is {0}'.format(node[i][0]))
					result = find_path(pgraph,s,node[i][0])
					nodes, edges, costs, total_cost = result
					if min_cost > result[3]:
						min_cost = result[3]
						clone = node[i][0]
						clone_number = i
						#  node[i].remove(0)
		
			print('startnode = {3},min cost is {0}, node is {1},clone_number is {2}'.format(min_cost,clone,clone_number,s))
			path.append(clone)
			node[clone_number].remove(clone)
			s=clone
			print(path)
			print('after node list is {0}'.format(node))
			min_cost = 10
		
		
		#  for i in node_list:
		#      result = find_path(pgraph,s,i)
		#      nodes, edges, costs, total_cost = result
		#      if min_cost > result[3]:
		#          min_cost = result[3]
		#          print(min_cost)



		return path
		

