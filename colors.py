# import random

# def generate_random_color():
#     # Generate random values for red, green, and blue components
#     red = random.randint(150, 255)  # Ensure a light color by setting a minimum value
#     green = random.randint(150, 255)
#     blue = random.randint(150, 255)

#     # Convert the RGB values to a hexadecimal color code
#     color_code = "#{:02X}{:02X}{:02X}".format(red, green, blue)

#     return color_code

# def generate_random_color_dictionary(num_colors):
#     color_dict = {}
#     for i in range(num_colors):
#         color_dict[str(i)] = generate_random_color()
#     return color_dict

# # Specify the number of random colors you want in the dictionary
# num_colors = 50  # Change this number as needed

# # Generate the dictionary of random HTML color codes
# color_dictionary = generate_random_color_dictionary(num_colors)

# # Print the resulting dictionary
# print(color_dictionary)


servers = [{'id': 0, 'start': 0, 'end': 2}, {'id': 1, 'start': 5, 'end': 7}, {'id': 2, 'start': 8, 'end': 9}, {'id': 3, 'start': 12, 'end': 14}, {'id': 4, 'start': 14, 'end': 17}, {'id': 5, 'start': 17, 'end': 18}, {'id': 6, 'start': 20, 'end': 22}, {'id': 7, 'start': 24, 'end': 25}, {'id': 8, 'start': 25, 'end': 26}, {'id': 9, 'start': 31, 'end': 33}, {'id': 10, 'start': 35, 'end': 38}, {'id': 11, 'start': 42, 'end': 43}, {'id': 12, 'start': 47, 'end': 49}]

color_dic = {'0': '#BBC69A', '1': '#DAA2E9', '2': '#D1A2F8', '3': '#ACC1B7', '4': '#E5EDDB', '5': '#EAF1DD', '6': '#A7CCC7', '7': '#AE97B0', '8': '#CAD8CB', '9': '#A2E8E2', '10': '#B3E8E1', '11': '#B3C2FC', '12': '#D3E29E', '13': '#EDC7C6', '14': '#CCF6FF', '15': '#D0EBCB', '16': '#D0D7F6', '17': '#A4E8EB', '18': '#A7E5AD', '19': 
'#9CF9B2', '20': '#DDDAA6', '21': '#A4A7CF', '22': '#A2A9BB', '23': '#AFD1D7', '24': '#C8A6CC', '25': '#E2F2A9', '26': '#FAD2D4', '27': '#BEBEE5', '28': '#ABD5B8', '29': '#DCB1D2', '30': '#E0D5EB', '31': '#FFDCDE', '32': '#9AE4A9', '33': '#BDA1BB', '34': '#D7C7E1', '35': '#CBC1E6', '36': '#AACDAB', '37': '#F8A7EE', '38': '#D0E5FF', '39': '#F5FBCD', '40': '#B2B5CF', '41': '#EBFAF8', '42': '#B3A5CC', '43': '#EDFCCA', '44': '#C7B4A6', '45': '#CFBAB1', '46': '#DFDABC', '47': '#EDBCEA', '48': '#A3A9C4', '49': '#D3C29E'}
def pic_color(servers):
    for i in range(len(servers)):
        a = servers[i]['id']
        servers[i]['color'] = color_dic[f'{a}']
    return servers    
