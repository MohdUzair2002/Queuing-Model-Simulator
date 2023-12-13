import atexit
from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64



from queuing_simulator.arrival_table import construct_avg_arrival_lookup_table
from queuing_simulator.simulator import Simulator
from queuing_simulator.queuing_formulae import calculate_averages_by_formula
from queuing_simulator.server_utilization import utl_rho, create_rho_dataframe
from queuing_simulator.hist_calculation import count
from queuing_simulator.total_average import write_or_append_to_csv, calculate_mean_last_six_columns, read_data_csv

from pprint import pprint
import pandas as pd

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
        
        if time_scale == "hr":
            arrival_mean = arrival_mean*60
            service_mean = service_mean*60
        elif time_scale == "sec":
            arrival_mean = arrival_mean/60
            service_mean = service_mean/60
        else:
            arrival_mean = arrival_mean
            service_mean = service_mean
            
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

       
        df_table = (sim.get_simulation_table())
        servers_lists = sim.get_servers_gantt_chart_data()
        server_with_priority = append_priority(servers_lists, df_table)
        servers = pic_color(servers_lists)
        averages = sim.calculate_averages()
        averages = averages[:-1]
        averages = average_converter(averages, time_scale)
        
        arrival_graph = line_graph(df_table)
        service_graph = bar_graph(df_table, 'service_time', 'Service Time')
        wait_graph = bar_graph(df_table,'wait_time','Wait Time')
        turn_around_graph = bar_graph(df_table,'turn_around_time', 'Turn Around Time')
        response_graph = bar_graph(df_table, 'response_time', 'Response Time')

        write_or_append_to_csv(float(arrival_mean), float(service_mean), num_of_servers, averages)
        hist_df = read_data_csv()
        print(hist_df)
        hist_average, page_count = calculate_mean_last_six_columns(hist_df)

        a, b = utl_rho(df_table, servers_lists)
        server_utilization_table = create_rho_dataframe(a,b)
        df_table = df_table.drop("inter_arrival_time", axis=1)
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
                           time_scale = time_scale,
                           arrival_graph = arrival_graph,
                           service_graph = service_graph,
                           wait_graph = wait_graph,
                           turn_around_graph = turn_around_graph,
                           response_graph = response_graph,
                           hist_average = hist_average,
                           page_count = page_count
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

def average_converter(averages, time_scale):
    if time_scale == 'sec':
        for i in averages:
            i['value'] = round(i['value']*60, 4)
    elif time_scale == 'hr':
        for i in averages:
            i['value'] = round(i['value']/60, 6)
    else:
        for i in averages:
            i['value'] = round(i['value'], 4)

    return averages


def bar_graph(df, y_xis_attr, ylabel):
    if 'priority' not in df.columns:
        df['priority'] = 0

    colors = np.where(df['priority'] == 1, '#FF4233',
                    np.where(df['priority'] == 2, '#FFE433', '#4FFF33'))

    df.plot(x='id', y=y_xis_attr, kind='bar', legend=False, color=colors)
    plt.xlabel('Customer ID')
    plt.ylabel(f'{ylabel} (min)')
    plt.title(f'{ylabel} for Each Customer')

    # Save the graph as an image and return image data
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    image_data = base64.b64encode(img.read()).decode("utf-8")
    return image_data

def line_graph(df):
    if 'priority' not in df.columns:
        df['priority'] = 0

    colors = np.where(df['priority'] == 1, '#FF4233', 
                    np.where(df['priority'] == 2, '#FFE433', '#4FFF33'))

    plt.figure(figsize=(8, 4))  # Adjust the figure size as needed

    # Plot lines between points
    for i in range(len(df) - 1):
        plt.plot([df['id'].iloc[i], df['id'].iloc[i + 1]], [df['arrival_time'].iloc[i], df['arrival_time'].iloc[i + 1]], marker='o', color=colors[i])

    plt.xlabel('Customer ID')
    plt.ylabel('Arrival Time (min)')
    plt.title('Customer Arrival Time')

    # Save the graph as an image in memory (BytesIO)
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    image_data = base64.b64encode(img.read()).decode("utf-8")
    return image_data

if __name__ == '__main__':
    app.run(debug=True)
