import random, pandas as pd

def utl_rho(df_simulation_table, servers):
    rho_list = []
    total_service_time = df_simulation_table['service_time'].sum()
    total_service_time_of_server = []
    total_service_time = 0
    for sublist in servers:
        server_service_time = sum(dictionary['end'] - dictionary['start'] for dictionary in sublist)
        total_service_time_of_server.append(server_service_time)
        total_service_time += server_service_time

    # Calculate and print individual rho values for each server
    for i, server_service_time in enumerate(total_service_time_of_server):
        rho = round(server_service_time / total_service_time, 3)
        rho_list.append(rho)
        # print(f'Rho Value of Server {i+1} = {rho}')

    # Calculate and print the sum of total rho values
    sum_rho = round(sum(total_service_time_of_server) / total_service_time, 3) - random.uniform(0.001, 0.009) 
    # rho_list, sum_rho ,
    return  total_service_time_of_server, total_service_time 



def create_rho_dataframe(total_service_time_of_server, total_service_time):
    rho_list = []
    for i, server_service_time in enumerate(total_service_time_of_server):
        rho = round(server_service_time / total_service_time, 3)
        rho = round(rho*100, 3) 
        rho = str(rho) + '%'

        server_name = f"Server {i+1}"
        rho_list.append([server_name, rho])

    df_rho = pd.DataFrame(rho_list, columns=["Server", "Utilization"])
    return df_rho