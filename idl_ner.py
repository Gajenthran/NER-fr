from util import Util
import re

class NER:
	def __init__(self, text, tagged_nodes):
		self.tagged_nodes = tagged_nodes
		self.text = text
		self.ner_obj = []
		self.dic = []

	def gen_models(self, model_filenames):
		models = {}
		for filename in model_filenames:
			d = ""
			d += Util.read_file(filename)
			lines = d.splitlines()
			models[lines[0]] = lines[1:]

		for key in models:
			self.dic.append(tuple((key, r"(?:" + Util.to_rgx(models[key])+ r")")))

		for i in range(0, len(self.tagged_nodes)):
			lst = [g[0] for g in self.tagged_nodes[i][1]]
			lst = r" ".join(lst)
			self.ner_obj.append([lst, self.tagged_nodes[i][0]])

	def use_models(self):
		for i in range(0, len(self.ner_obj)):
			for d in self.dic:
				if self.ner_obj[i][0] == "NER-Obj":
					for m in re.finditer(
						d[1], self.ner_obj[i][1]
					):
						self.ner_obj[i][0] = d[0]

		for ner in self.ner_obj:
			print(ner)

	def filter_ner(self):
		lst = []

		for ner in self.ner_obj:
			for m in re.finditer(r"\b" + ner[0] + r"\b", self.text):
				lst.append(tuple((m.group(), ner[1], m.start(), m.end())))
		lst = sorted(list(set(lst)), key=lambda x: x[2])
		self.ner_obj = lst

	def apply(self):
		self.use_models()
		self.filter_ner()

	def get_ner(self):
		return self.ner_obj