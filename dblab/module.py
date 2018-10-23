import pymysql
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths

class Tests:



#make graph module ( from drive course )
#  ------------------------------------------------------------
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



# find startnode with latitude, longitude which receive from ros
#---------------------------------------------------------------------------------------------
	def find_start_node(self, data_list):

		con = pymysql.connect(host='localhost', user='root', password='1', db='jcm_drive', charset='utf8')


		curs = con.cursor()

		fromnode_sql = "select fromnode, tonode from drive2.a3_link where linkid="
		tonode_sql = "select tonode from drive2.a3_link_view where fromnode= "
		print(fromnode_sql+"'" +data_list[0]+"';")
		curs.execute(fromnode_sql+"'" +list(data_list)[0]+"';")

		fromnode_row= curs.fetchall() 
		for i in fromnode_row:
			fromnode=list(map(lambda x:x, i))
		print("fromnode:"+fromnode[1])
		data_list.remove(data_list[0])
		
		return fromnode





#find link_id, fromnode, and inputnode which input to find_short_path module 
#----------------------------------------------------------------------------------------

	def find_insert_node(self,count,data_list):
		
		con = pymysql.connect(host='localhost', user='root', password='1', db='jcm_drive', charset='utf8')


		curs = con.cursor()

		tonode_sql = "select tonode from drive2.a3_link where linkid="
		inputnode_list = []
		for i in range(0,count,2):

			linkid_sql = "SELECT ono, MIN(6371*acos(cos(radians({0}))*cos(radians(gps.lat))*cos(radians(gps.lon) - radians({1})) + sin(radians({2}))*sin(radians(gps.lat)))) AS distance FROM jcm_drive.gps where id like 'A3%' group by id order by distance limit 1".format(data_list[i],data_list[i+1],data_list[i])
			print( "SELECT ono, MIN(6371*acos(cos(radians({0}))*cos(radians(gps.lat))*cos(radians(gps.lon) - radians({1})) + sin(radians({2}))*sin(radians(gps.lat)))) AS distance FROM jcm_drive.gps where id like 'A3%' group by id order by distance limit 1, number is {3}".format(data_list[i],data_list[i+1],data_list[i],i))
			curs.execute(linkid_sql)
			link_id_row = curs.fetchall()
			link_id = list(map(lambda x:x, link_id_row[0]))
			print('link_id : {0}'.format(link_id[0]))
			curs.execute(tonode_sql+"'" +link_id[0]+"';")

			tonode_row= curs.fetchall()
			for j in tonode_row:
				tonode=list(map(lambda x:x, j))

			print('tonode : {0}'.format(tonode[0]))
			
			inputnode_list.append(tonode[0])
			print('inputnode = {0}'.format(tonode[0]))

		return inputnode_list



#  return tonode, length, and nodeid from shortest path
#----------------------------------------------------------------------
	def result_msg(self,nodes):
		
		con = pymysql.connect(host='localhost', user='root', password='1', db='jcm_drive', charset='utf8')
		result_string = ''

		curs = con.cursor()
			
		print('node is {0}'.format(nodes))
		for i in range(1,len(nodes)):
			etc_info_sql = "select length from jcm_drive.a3_link_view where fromnode ='{0}' and tonode='{1}' ;".format(nodes[i-1],nodes[i])

			print(etc_info_sql)
			#  pop_index=nodes.pop(0)
			curs.execute(etc_info_sql)
			etc_info_sql_row = curs.fetchall()
			for j in etc_info_sql_row:
				etc_info=list(map(lambda x:x, j))
				print("etc_info_row 0 : {0}".format(etc_info[0]))
				result_string+=" {0} {1} 0000".format(str(nodes[i]),str(etc_info[0]))

		return result_string
		



#find_short_path use dijkstar package 
#and return shortest node from startnode
#----------------------------------------------------------------

	def find_short_path(self,pgraph,s,node_list):
		path =[]
		node=[]
		min_cost = 1000
		count = 0
		path_count=0
		print(node_list)
		for i in range(len(node_list)):
				print('check node is {0}'.format(node_list[i]))
				result = find_path(pgraph,s,node_list[i])
				nodes, edges, costs, total_cost = result
				if min_cost > total_cost:
					min_cost = total_cost
					clone = node_list[i]
		
		print('startnode = {2},min cost is {0}, node is {1}'.format(min_cost,clone,s))
		path.append(clone)
		print(path)
		print('after node list is {0}'.format(path))
		for i in path:
			path_result=list(map(lambda x:x, i))
		


		return str(path[0])
		

