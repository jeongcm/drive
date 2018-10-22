import pymysql
import sys
import socket
from dijkstar import find_path, NoPathError, Graph
from dijkstar.algorithm import single_source_shortest_paths
import module
from collections import OrderedDict

class TcpHandler():
 	
	#  def handle(self):
	#      print("client ip : {0}".format(self.client_address[0]))
	#      sock = self.request
    #
	#      __recv_msg = sock.recv(1024)
    #
	#      recv_message= str(__recv_msg, encoding='utf-8')
    #
	#      print("recv: {0}".format(recv_message))
	#  메시지 보낼때는 직접 리스트를 pickle.dump이용해서 빼낸다음 하나씩 보낼 예정
	def send_msg(self,result_list):
		ip = sys.argv[1]
		port = 7429
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connet((ip,port))
			for data  in result_list:
				print('module send data : {0}'.format(data))
				s.sendall(data)

class passenger():

		def find_default_path(self, pgraph,s,clone_node):
			con = pymysql.connect(host='localhost', user='root', password='1', db='drive2', charset='utf8')

			curs = con.cursor()
		
			# '155M10640204', 155M10660204, 155M10680204, 155M10690204,155M10720204,155M10740204, 155M10760204, 155M10790204a
			node_list = []
			result_path= []
			node = ['155M10720204','155M10740204','155M10810204']
			path=module.Tests()
			result = path.find_short_path(pgraph,s,node)
			node_list+=result
			for path_node in node_list:
				path_result =find_path(pgraph,s,path_node)

				nodes,edges,costs,total_cost = path_result
				#  print(nodes)
				result_path+=nodes
				s= path_node
			#  destination_result = find_path(pgraph,s,d)
			#  nodes,edges,costs,total_cost = destination_result
			#  result_path +=nodes
			#  OrderedDict.fromkeys(result_path)
			return result_path


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('{0} <BIND IP>'.format(sys.argv[0]))
		sys.exit()
	con = pymysql.connect(host='localhost', user='root', password='1', db='jcm_drive', charset='utf8')

	curs = con.cursor()
		
	fromnode_sql = "select fromnode from drive2.a3_link ono="
	tonode_sql = "select tonode from drive2.a3_link_view where fromnode= "
	etc_info_sql = "select tonode, length from jcm_drive.a3_link_view where fromnode = "
	graph_object=module.Tests()
	r_graph = graph_object.make_graph()
	ip = sys.argv[1]
	port = 7429
	print('{0} server start'.format(ip))
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, port))
		#  print('Connected by', addr)
		while True:
				s.listen(1)
				conn, addr = s.accept()
				inputnode_list=[]
				result_string = ""
				data = conn.recv(1024)
				if not data :
					continue
				print(data)
				#  data_list = data.split('/')
				#  curs.execute(fromnode_sql+"'" +data_list[0]+"';")
				#  fromnode_row= curs.fetchall()
				#  fromnode=list(map(lambda x:x, fromnode_row))
				#  curs.execute(tonode_sql+"'" +fromnode[0]+"';")
				#  startnode_row=curs.fetchall()
				#  startnode=list(map(lambda x:x, startnode_row))
				#  print('startnode = {0}'.format(startnode[0]))
				#  data_list.remove(data_list[0])
				#  for i in range(2):
				#      linkid_sql = "SELECT ono, MIN(6371*acos(cos(radians({0}))*cos(radians(gps.lat))*cos(radians(gps.lon) - radians({1})) + sin(radians({2}))*sin(radians(gps.lat)))) AS distance FROM jcm_drive.gps where id like 'A3%' group by id order by distance limit 1".format(data_list[i],data_list[i+1],data_list[i]);
				#      curs.execute(linkid_sql)
				#      link_id_row = curs.fetchall()
				#      link_id = list(map(lambda x:x, link_id_row[0]))
				#      print('link_id : {0}'.format(link_id[0]))
				#      curs.execute(fromnode_sql+"'" +link_id[0]+"';")
				#      fromnode_row= curs.fetchall()
				#      fromnode=list(map(lambda x:x, fromnode_row))
				#      print('fromnode : {0}'.format(fromnode[0]))
				#      curs.execute(tonode_sql+"'" +fromnode[0]+"';")
				#      input_node_row=curs.fetchall()
				#      input_node=list(map(lambda x:x, input_node_row))
				#      i+=1
				#      inputnode_list+=input_node[0]
				#      print('inputnode = {0}'.format(input_node[0]))
                #
				#  ps = passenger()
				#  nodes = ps.find_default_path(r_graph,startnode[0],inputnode_list)
				#  for i in range(len(nodes)):
				#          pop_index=nodes.pop(0)
				#          result_string+=str(pop_index)
				#          curs.execute(etc_info_sql+"'" +pop_index+"';")
				#          etc_info_sql_row = curs.fetchall()
				#          print("etc_info_row 0 : {0} . etc_info_row1 : {1}".format(etc_info_sql_rowl[0],etc_info_sql_row[1]))
				#          result_string+=" "
				#          result_string+=str(etc_info_sql_row[0])
				#          result_string+=" "
				#          result_string+=str(etc_info_sql_row[1])
				#          result_string+=" "
				#  print(result_string)


