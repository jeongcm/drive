import pymysql
import unittest
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths
class Tests(unittest.TestCase):
	#database에서 sql 문으로 노드아이디 불러옴
	def make_graph(self):

		con = pymysql.connect(host='localhost', user='root', password='1', db='drive2', charset='utf8')


		curs = con.cursor()

		graph = Graph()
		sql = "select nodeid from drive2.c1_node"
		sql2 = "select tonode, length, format(speed,0) from drive2.a3_link, jcm_drive.jcm_a3_link where fromnode = "

		curs.execute(sql)

		rows= curs.fetchall()
		for i in rows:
			nodeid= list(map(lambda x:x,i))
			curs.execute(sql2+"'" +nodeid[0]+"';")

			rows=curs.fetchall()

			if rows is None:
				continue
			else:
				for item in list(rows):
					cost = item[1]/int(item[2])
					graph.add_edge(i[0], item[0], cost)

		con.close()
		return graph
	
	#지금은 매개변수가 self.랑 pgraph가 다인데 아마 실제 함수쓸때 startnode와 destinationnode 각각 매개변수로 넣어줘야함으로 
	#함수에 매개변수 추가해야할것
	#추가로 socke 함수 구현 필요
	def test_find_path(self, pgraph):

		result = find_path(pgraph,'155M10640204','155M10690204')
		print(list(result[0]))


r_graph = Tests()
result =r_graph.make_graph()
result2 = Tests()
result2.test_find_path(result)


