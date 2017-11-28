import csv
import textwrap
import sys

iching_data_path = "ichingdata.csv"

def deesc(s):
	return bytes(s, "utf-8").decode("unicode_escape")

class Hexagram(object):
	def __init__(self, row):
		self.hexagram = row["hexagram"]
		self.judgement = deesc(row["judgement"])
		self.first_change = deesc(row["first_change"])
		self.second_change = deesc(row["second_change"])
		self.third_change = deesc(row["third_change"])
		self.fourth_change = deesc(row["fourth_change"])
		self.fifth_change = deesc(row["fifth_change"])
		self.sixth_change = deesc(row["sixth_change"])
		self.image = deesc(row["image"])
		self.title = deesc(row["title"])
	def __str__(self):
		return "Hexagram(\"{}\", \"{}\")".format(self.hexagram, self.title)

def get_drawing(c):
	if c == "0":
		return "- -"
	else:
		return "---"
		
class Change(object):
	def __init__(self, data, change):
		self.old = get_hexagram(data, get_old_hexagram_string(change))
		self.new = get_hexagram(data, get_new_hexagram_string(change))
		
		self.changes = []
		cs = "96"
		if change[0] in cs:
			self.changes.append(self.old.first_change)
		if change[1] in cs:
			self.changes.append(self.old.second_change)
		if change[2] in cs:
			self.changes.append(self.old.third_change)
		if change[3] in cs:
			self.changes.append(self.old.fourth_change)
		if change[4] in cs:
			self.changes.append(self.old.fifth_change)
		if change[5] in cs:
			self.changes.append(self.old.sixth_change)
	def get_diagram(self):
		if len(self.changes):
			return "\n".join("   {}  ->  {}".format(get_drawing(o), get_drawing(n)) for (o,n) in zip(self.old.hexagram[::-1], self.new.hexagram[::-1]))
		else:
			return "\n".join("   {}".format(get_drawing(l)) for l in self.old.hexagram)
	def pretty_print(self):
		if len(self.changes):
			print(textwrap.dedent("""{}
moves to
{}

{}

Image:
{}

Judgement:
{}

Changes:
{}

Future Image:
{}

Future Judgement:
{}""".format(self.old.title, self.new.title, self.get_diagram(), self.old.image, self.old.judgement, "\n".join(self.changes), self.new.image, self.new.judgement)))
		else:
			print(textwrap.dedent("""Static: {}

{}

Image:
{}

Judgement:
{}""".format(self.old.title, self.get_diagram(), self.old.image, self.old.judgement)))

		
		
def get_iching_data():
	data = {}
	with open(iching_data_path, "r") as f:
		rdr = csv.DictReader(f, delimiter=",", quotechar = "\"")
		for row in rdr:
			data[row["hexagram"]] = Hexagram(row)
	return data
	
	
def get_old_char(chg):
	if chg == "6" or chg == "8":
		return "0"
	else:
		return "1"
	
def get_new_char(chg):
	if chg == "6" or chg == "7":
		return "1"
	else:
		return "0"
	
def get_old_hexagram_string(change):
	return "".join(get_old_char(c) for c in change)
	
def get_new_hexagram_string(change):
	return "".join(get_new_char(c) for c in change)
	
def get_hexagram(data, hex_string):
	return data[hex_string]

if __name__=="__main__":
	if len(sys.argv) < 2:
		print("No change provided")
	else:
		data = get_iching_data()
		change = Change(data, sys.argv[1])
		change.pretty_print()
