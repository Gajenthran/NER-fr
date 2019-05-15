from util import Util
import re

class NER:
	def __init__(self, text, tagged_nodes):
		self.tagged_nodes = tagged_nodes
		self.text = text
		self.ner_obj = []
		self.dic = []

	def check(self):
		for i in range(0, len(self.tagged_nodes)):
			if self.tagged_nodes[i][0] == "NER-Date" and not(self.check_date(i)):
				self.tagged_nodes[i] = 0
			# if self.tagged_nodes[i][0] == "NER-Loc":
			#  	self.tagged_nodes[i][1] = [tuple((self.tagged_nodes[i][1][-1][0], "NER-Loc"))]
			#  	self.tagged_nodes[i][0] = "NER-Loc"
		Util.rm_duplicate(self.tagged_nodes)

	def gen_models(self, model_filenames):
		models = {}
		for filename in model_filenames:
			d = ""
			d += Util.read_file(filename)
			lines = d.splitlines()
			models[lines[0]] = lines[1:]

		for key in models:
			self.dic.append(tuple((key, r"(?:" + Util.to_rgx(models[key])+ r")")))

	def create_ner(self):
		for i in range(0, len(self.tagged_nodes)):
			lst = [g[0] for g in self.tagged_nodes[i][1]]
			lst = r" ".join(lst)
			self.ner_obj.append([lst, self.tagged_nodes[i][0]])

	def check_date(self, index):
		day = False
		checked = True
		for tag in self.tagged_nodes[index][1]:
			if day == True and tag[1] == "Lnumber":
				if int(tag[0]) > 0:
					break
				else:
					checked = False
					break
			if tag[1] == "Lnumber":
				if 1 < int(tag[0]) < 31:
					day = True
				else:
					checked = False
					break
		return checked

	def use_models(self):
		for i in range(0, len(self.ner_obj)):
			for d in self.dic:
				if self.ner_obj[i][1] == "NER-Obj":
					for m in re.finditer(
						d[1], self.ner_obj[i][0]
					):
						self.ner_obj[i][1] = d[0]

	def filter_ner(self):
		lst = []
		for ner in self.ner_obj:
			for m in re.finditer(r"\b" + ner[0] + r"\b", self.text):
				lst.append(tuple((m.group(), ner[1], m.start(), m.end())))
		# lst = Util.sort_ner(lst)
		lst = sorted(list(set(lst)), key=lambda x: x[2])
		# lst = Util.prioritize_obj(lst)
		self.ner_obj = lst

	def apply(self):
		self.check()
		self.create_ner()
		self.use_models()
		self.filter_ner()

	def get_ner(self):
		return self.ner_obj