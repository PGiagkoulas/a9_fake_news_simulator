# script to generate experiment files

def main():
	fileCount = 1
	conn_list = ["random", "cluster", "sun"]
	comm_list = ["random", "SYO", "CO", "LNS"]
	conv_list = ["discussion", "majority_opinion", "simple"]
	
	for connectivity_type in conn_list:
		for comm_protocol in comm_list:
			for conv_protocol in conv_list:
				fileName = "exp" + str(fileCount) + ".txt"
				with open(fileName, 'w') as writer:
					writer.write("n_agents 100 \nn_liars 5 \nn_experts 5 \nn_connections 3000 \ncluster_distance 0 \n")
					writer.write("n_news 1 \nn_steps 50 \n")
					writer.write("connectivity_type " + connectivity_type + "\n")
					writer.write("communication_protocol " + comm_protocol + "\n")
					writer.write("conversation_protocol " + conv_protocol + "\n")
					writer.write("runs 100")
				fileCount += 1
if __name__ == "__main__":
	main()
