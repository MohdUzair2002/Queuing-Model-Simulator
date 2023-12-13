import csv

def write_or_append_to_csv(a, s, n, averages):
    data_to_write = [a, s, n] + [item["value"] for item in averages]

    try:
        # Try to open the CSV file for reading
        with open("data.csv", "r", newline="") as file:
            reader = csv.reader(file)

            # Check if the file is not empty
            for row in reader:
                if row[:3] == [str(a), str(s), str(n)]:
                    # First elements match, append the data and exit
                    with open("data.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data_to_write)
                    return

        # If no match is found, remove the existing data and write a new row
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            headers = ["a", "s", "n"] + [item["name"] for item in averages]
            writer.writerow(headers)
            writer.writerow(data_to_write)

    except FileNotFoundError:
        # File doesn't exist, create it and write a new row
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            headers = ["a", "s", "n"] + [item["name"] for item in averages]
            writer.writerow(headers)
            writer.writerow(data_to_write)
import pandas as pd

def read_data_csv():
    try:
        # Attempt to read the CSV file into a DataFrame
        df = pd.read_csv("data.csv")
        return df
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print("File 'data.csv' not found.")
        return None

def calculate_mean_last_six_columns(df):
    if df is not None:
        last_six_columns = df.iloc[:, -6:]
        mean_values = last_six_columns.mean().to_dict()
        return [{'name': key, 'value': value} for key, value in mean_values.items()]
    else:
        return None

# Example usage



# Example usage




# Example usage
averages = [{'name': 'Average Inter Arrival Time', 'value': 2.0}, {'name': 'Average Service Time', 'value': 3.5}, {'name': 'Average Turn Around Time (Ws)', 'value': 4.5}, {'name': 'Average Wait Time (Wq)', 'value': 12.0}, {'name': 'Length of system (Ls)', 'value': 2.105263157894737}, {'name': 'Length of queue (Lq)', 'value': 0.0}]
a = 1.0
s = 3.2
n = 3

data_frame = read_data_csv()

if data_frame is not None:
    mean_last_six_columns = calculate_mean_last_six_columns(data_frame)
    if mean_last_six_columns is not None:
        print("Mean of the last six columns:")
        print(mean_last_six_columns)
    else:
        print("No data to calculate the mean.")