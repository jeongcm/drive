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
			node = [" 155M10720204","155M10740204","155M10810204"]
			path=module.Tests()
			result = path.find_short_path(pgraph,s,clone_node)
			path_result =find_path(pgraph,s,result)
			nodes,edges,costs,total_cost = path_result
				#  print(nodes)
			result_path+=nodes


			#  destination_result = find_path(pgraph,s,d)
			#  nodes,edges,costs,total_cost = destination_result
			#  result_path +=nodes
			#  OrderedDict.fromkeys(result_path)
			print("result path {0}".format(result_path))
			return result_path


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('{0} <BIND IP>'.format(sys.argv[0]))
		sys.exit()
	graph_object=module.Tests()
	r_graph = graph_object.make_graph()
	ip = sys.argv[1]
	port = 7429
	print('{0} server start'.format(ip))
	node_module = module.Tests()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, port))
		while True:
				s.listen(1)
				conn, addr = s.accept()
				data = conn.recv(1024)
				if not data :
					continue
				print('before data : {0}'.format(data))
				data.decode("utf-8","strict")

				print('after data : {0}'.format(data))

				#  data_list = data.split('/')
				data_list = ['155M1044ZZ0204','35.8392214','128.6842610','35.8393099','128.6835070']
				print(data_list[0])
				startnode=node_module.find_start_node(data_list)
				print('startnode= '+startnode[1])
				inputnode_list = node_module.find_insert_node(len(data_list),data_list)

				ps = passenger()
				nodes = ps.find_default_path(r_graph,str(startnode[1]),inputnode_list)
				nodes.insert(0,str(startnode[0]))
				result = node_module.result_msg(nodes)
				result_msg = bytes(result, encoding='utf-8')
				print(result_msg)
				conn.send(result_msg)


