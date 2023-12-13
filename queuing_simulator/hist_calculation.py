def count(arrival_mean, service_mean, averages):
    average_list = []
    a_mean = []
    s_mean = []
    if len(a_mean) == 0 and len(s_mean) == 0:
        a_mean.append(arrival_mean)
        s_mean.append(service_mean)
        average_list.append(averages)
    elif a_mean[0] == arrival_mean and s_mean[0] == service_mean:
        a_mean.append(arrival_mean)
        s_mean.append(service_mean)
        average_list.append(average_list)
    else:
        a_mean.clear()
        s_mean.clear()
    return average_list, len(s_mean)

def extract_value(h_list, count):
    hf_list = []
    for i in range(count):
        av_list =[]
        for j in range(6):
            av_list.append(h_list[i][j]['value'])
        hf_list.append(av_list)
    return hf_list

def add_list_elements(lists):
    if not lists:
        return []
    # Use zip to group corresponding elements in the inner lists
    result = [sum(values) for values in zip(*lists)]

    return result

def divide_list_by_number(input_list, divisor):
    if divisor == 0:
        raise ValueError("Division by zero is not allowed")

    result = [element / divisor for element in input_list]
    return result


# result =divide_list_by_number(add_list_elements(extract_value(a, 2)), 2)
# print(result)

