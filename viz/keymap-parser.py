import os
from typing import List
from pprint import pprint
from prettytable import PrettyTable, ALL
from bs4 import BeautifulSoup

symbol_list = ["ltog", "lto", "mto", "mtp", "kp", "lt", "mt", "bt"] # NB order matters! Longest first.
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

def keymap_to_dict():
	with open("/home/marco/Github/zmk-config/config/kyria.keymap", "r") as f:
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
			kc += len(row)

	# Pad the rows so we have a neat grid
	for name in processed_keymap.keys():
		processed_keymap[name] = pad_rows(processed_keymap[name])
	print("Layers:", layer_names)
	print(len(processed_keymap), "rows of keys.")
	print(kc, "total keys (including &trans)")
	print()
	return processed_keymap

def pad_rows(layer):
	# Turn into a 4x16 grid so we can pretty print it
	# top two layers need 2 extra keys on the inside
	# bottom thumb tow needs three extra keys on the outside
	result = layer.copy()
	result[0] = layer[0][:6] + ["", ""] + ["", ""] + layer[0][6:]
	result[1] = layer[1][:6] + ["", ""] + ["", ""] + layer[1][6:]
	result[3] = ["", "", ""] + layer[3][:6] + layer[3][6:] + ["", "", ""]
	return result

def keymap_dict_to_console(processed_keymap):
	# ASCII art
	# # Pad the rows so we have a neat grid
	# for name in processed_keymap.keys():
	# 	processed_keymap[name] = pad_rows(processed_keymap[name])

	# Print the table to console
	for name, layer in processed_keymap.items():
		table = PrettyTable(hrules=ALL, header=False)
		table.add_rows(layer)
		print(name)
		print(table)
		print()

def keymap_dict_to_html(processed_keymap, dir="output/"):
	"""
	Build a single html file from each table's html str
	"""
	table = PrettyTable(hrules=ALL, header=False)
	layers =  list(processed_keymap.keys())
	layer_name = layers[0]  # First build table for layer 0
	table.add_rows(processed_keymap[layer_name])
	html_str = table.get_html_string(format=True)
	soup = BeautifulSoup(html_str, 'html.parser')

	tr = soup.new_tag("tr")
	td = soup.new_tag("td")
	td.attrs["colspan"] = 16
	h = soup.new_tag("h4")
	h.string = layer_name
	td.append(h)
	tr.append(td)
	soup.table.tr.insert_before(tr) # insert as first row in table

	# Append rows to existing html table
	for layer_name in layers[1:]:
		table = PrettyTable(hrules=ALL, header=False)
		table.add_rows(processed_keymap[layer_name])
		html_str = table.get_html_string(format=True)
		curr_soup = BeautifulSoup(html_str, 'html.parser')
		tr = curr_soup.new_tag("tr")
		td = curr_soup.new_tag("td")
		td.attrs["colspan"] = 16
		h = curr_soup.new_tag("h4")
		h.string = layer_name
		td.append(h)
		tr.append(td)
		curr_soup.table.tr.insert_before(tr) # insert as first row in table
		for tr in curr_soup.find_all("tr"):
			soup.find_all("tr")[-1].insert_after(tr)
		
	# Inject js to highlight mod keys, layers, etc
	with open("keymap-viz.js", "r") as f:
		script = soup.new_tag("script")
		script.string = f.read()
		soup.append(script)

	path = os.path.join(dir, "output.html")
	with open(path, "w", encoding = 'utf-8') as file:    
		file.write(str(soup.prettify()))
		print("Saved:", path)

def keymap_dict_to_json(processed_keymap, dir="output"):
	with open("kyria-template.json", "r") as f:
		template = f.read()

	for name, layer in processed_keymap.items():
		result = template  # copy the template
		layer = pad_rows(layer)
		for i, row in enumerate(layer):
			for j, key in enumerate(row):
				if key == "trans" or key == "":
					key = "0"
				# print(f"{i},{j:02}", key.__repr__().replace("'", ""), key)
				result = result.replace(f"{i},{j:02}", key.__repr__().replace("'", ""))

		path = os.path.join(dir, f"kyria-{name}.json")
		with open(path, "w") as f:
			f.write(result)
		print(path)

if __name__ == '__main__':
	km = keymap_to_dict()
	# keymap_dict_to_console(km)
	keymap_dict_to_html(km)
	keymap_dict_to_json(km)
	# pprint(processed_keymap, compact=True, width=200, sort_dicts=False)
