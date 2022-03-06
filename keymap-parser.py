from typing import List
from pprint import pprint
from prettytable import PrettyTable, ALL
from bs4 import BeautifulSoup

symbol_list = ["lto", "mto", "kp", "lt", "mt", "bt"] # NB order matters! Longest first.
def remove_symbols(arr: List[str]):
	result = []
	for s in arr:
		s = s.strip()
		for symbol in symbol_list:
			s = s.replace(symbol, "").strip()  # delete symbol

		if s != "": # Only append if its a non empty string at this point
			if "BT_SEL" not in s:
				# if there are two keys, replace first space with newline
				# BT_SEL is a special case that takes an argument
				s = s.replace(" ", "\n", 1)
			result.append(s) 
	return result


with open("/Users/mchris/zmk-config/config/kyria.keymap", "r") as f:
	data = f.readlines()

layer_names = [l.split("#define ")[1].strip().split()[0] for l in data if "#define" in l]

idx = [i for i, s in enumerate(data) if "keymap {" in s][0]

layers = []
for i in range(idx, len(data)):
	line = data[i]
	if "\tbindings = " in line:
		layer = data[(i+1):(i+5)]
		layers.append(layer)

processed_keymap = {}
for name, layer in zip(layer_names, layers):
	temp = []
	for line in layer:
		if line != "\n":
			keys = line.split("&")
			key_list = remove_symbols(keys)
			temp.append(key_list)
	processed_keymap[name] = temp
kc = 0
for layer in processed_keymap.values():
	for row in layer:
		print(len(row))
		kc += len(row)
	print()

print("Layers:", layer_names)
print(len(processed_keymap), "rows of keys.")
print(kc, "total keys (including &trans)")
pprint(processed_keymap, compact=True, width=200, sort_dicts=False)

def pad_rows(layer):
	# Turn into a 4x16 grid so we can pretty print it
	# top two layers need 2 extra keys on the inside
	# bottom thumb tow needs three extra keys on the outside
	result = layer.copy()
	result[0] = layer[0][:6] + ["", ""] + ["", ""] + layer[0][6:]
	result[1] = layer[1][:6] + ["", ""] + ["", ""] + layer[1][6:]
	result[3] = ["", "", ""] + layer[3][:6] + layer[3][6:] + ["", "", ""]
	return result

# ASCII art part
# Pad the rows so we have a neat grid
for name in processed_keymap.keys():
	processed_keymap[name] = pad_rows(processed_keymap[name])

# Print the table to console
for name, layer in processed_keymap.items():
	table = PrettyTable(hrules=ALL, header=False)
	table.add_rows(layer)
	print(name)
	print(table)
	print()

# Built a single html file from each table's html str
# First build a table for layer 0
table = PrettyTable(hrules=ALL, header=False)
layer_name = layer_names[0]
table.add_rows(processed_keymap[layer_name])
html_str = table.get_html_string(format=True)
soup = BeautifulSoup(html_str, 'html.parser')
h = soup.new_tag("h4")
h.string = layer_name
soup.table.insert_before(h)


for layer_name in layer_names[1:]:
	table = PrettyTable(hrules=ALL, header=False)
	table.add_rows(processed_keymap[layer_name])
	html_str = table.get_html_string(format=True)
	curr_soup = BeautifulSoup(html_str, 'html.parser')
	h = curr_soup.new_tag("h4")
	h.string = layer_name
	curr_soup.table.append(h)
	print(len(soup.find_all("table")))
	soup.find_all("table")[-1].insert_after(curr_soup.table)	

with open("output.html", "w", encoding = 'utf-8') as file:    
    file.write(str(soup.prettify()))
	
