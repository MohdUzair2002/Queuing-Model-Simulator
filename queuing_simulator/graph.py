import atexit
from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, request, jsonify
from flask_cors import CORS

from queuing_simulator.arrival_table import construct_avg_arrival_lookup_table
from queuing_simulator.simulator import Simulator
from queuing_simulator.queuing_formulae import calculate_averages_by_formula
from queuing_simulator.server_utilization import utl_rho, create_rho_dataframe
from queuing_simulator.hist_calculation import count

from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    queue_type = request.form['queueType']
    if queue_type == '1':
        
        interarrival_distribution = request.form['interarrivalDistributionPriority']
        arrival_mean = eval(request.form['arrivalMean1'])
        num_of_servers = int(request.form['num_of_servers1'])
        service_distribution = request.form['serviceDistributionPriority']
        service_mean = eval(request.form['serviceMean1'])
        time_scale = str(request.form['time'])
        # a = eval( request.form['a'])
        # c = eval(request.form['c'])
        # m = eval(request.form['m'])
        
        # Add more variables for Priority queue if needed
        
        sim = Simulator(
            num_of_servers,
            0,
            arrival_mean,
            0,
            service_mean,
            55,
            9,
            1994,
            is_priority_based=True,
        )
        sim.run()

        print(time_scale)
        df_table = (sim.get_simulation_table())
        line_graph(df_table)
        bar_graph(df_table,"service_time","Service Time")
        bar_graph(df_table,"wait_time","Wait Time")
        bar_graph(df_table,"turn_around_time","Turn Around Time")
        bar_graph(df_table,"response_time","Response Time")

        servers_lists = sim.get_servers_gantt_chart_data()
        server_with_priority = append_priority(servers_lists, df_table)
        servers = pic_color(servers_lists)
        averages = sim.calculate_averages()
        averages = averages[:-1]
        averages2 =  averages
        a, b = utl_rho(df_table, servers_lists)
        server_utilization_table = create_rho_dataframe(a,b)
        df_table = df_table.to_html(index=False)
        server_utilization_table = server_utilization_table.to_html(index=False)

    else:
        interarrival_distribution = request.form['interarrivalDistribution']
        arrival_mean = eval(request.form['arrivalMean'])
        # num_of_servers = int(request.form['num_of_servers'])
        service_distribution = request.form['serviceDistribution']
        service_mean = eval(request.form['serviceMean'])
        
    return render_template('result.html',
                           arrival_mean = arrival_mean,
                           service_mean = service_mean,
                           servers=servers,
                           df_table=df_table,
                           averages=averages,
                           server_utilization_table=server_utilization_table,
                           averages2 = averages2
                           )




color_dic = {'1': '#FF4233', '2': '#FFE433', '3': '#4FFF33'}




def append_priority(server_list,df):
    for servers in server_list:    
        for i in range(len(servers)):
            a = servers[i]['id']
            priority = df.loc[df['id'] == a, 'priority'].values[0]
            servers[i]['priority'] = f"{priority}"
    return server_list 
    


def pic_color(server_list):
    for servers in server_list:    
        for i in range(len(servers)):
            a = servers[i]['priority']
            servers[i]['color'] = color_dic[f'{a}']
    return server_list    


def bar_graph(df,y_xis_atr,ylabel):

    if 'priority' not in df.columns:
        df['priority'] = 0

    colors = np.where(df['priority'] == 1, '#FF4233', 
                    np.where(df['priority'] == 2, '#FFE433', '#4FFF33'))

    df.plot(x='id', y=y_xis_atr, kind='bar', legend=False, color=colors)
    plt.xlabel('Customer ID')
    plt.ylabel(f'{ylabel} (min)')
    plt.title(f'{ylabel} for Each Customer')
    return plt.show()

def line_graph(df):
    plt.plot(df['id'], df['arrival_time'], marker='o')
    plt.xlabel('Customer ID')
    plt.ylabel('Arrival Time')
    plt.title('Customer Arrival Time')
    return plt.show()




if __name__ == '__main__':
    app.run(debug=True)
