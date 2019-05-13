from util import Util
import re

class NER:
	PONCT = r'(?:—|-|\.|!|\?|«|"|\')'
	RULES = [
		(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", "NER-Mail"),
		(r'(0[0-9]|1[0-9]|2[0-3]|[0-9])(?:\s*h\s*|\s*:\s*)[0-5][0-9]', "NER-Time"),
		(r'(\d+)\s*(?:heures|heure|h|minute\w*|min|\w*seconde\w*|sec)', "NER-Time"),
		(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),
		(r'([0-2][0-9]|(3)[0-1])(?:\/|-)(((0)[0-9])|((1)[0-2]))(?:\/|-)\d{4}', "NER-Date"),
		(r"(?:-|\+)?\d*(?:\.|,)?\d+", "NER-Number"), # en lettre
		(r"(?<!" + PONCT + r"\s)(?!^)\b([A-Z]\w*(?:(?:\s|-|\.|'|’)[A-Z]\w*)*)", "NER-Obj"),
		# (r"(?=[A-Z]\w*(?:\s+[A-Z]\w*)*)(?!" + gram_words + r")(?:[A-Z]\w*(?:\s+[A-Z]\w*)*)", "NER-Obj"),
		(r"[a-z]+(?:-|\.|'|’)?[A-Z0-9]\w*", "NER-lowerCamelCase"),
		(r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*', "NER-upperCamelCase"),
		# (r"(?:" + lst_exprs(trained_dic["NER-Day"]) + r")", "NER-Day"),
		# (r"(?:" + lst_exprs(trained_dic["NER-Person"]) + r")", "NER-Person"),
		# (r"((3[01]|[12][0-9]|[1-9])\s+)?(?:" + lst_exprs(trained_dic["NER-Month"]) + r")\s+\d+", "NER-Date"),
		# (r"(?:" + lst_exprs(trained_dic["NER-Sugg"]) + r")", "NER-Sugg"),
	]

	def __init__(self, text):
		self.dic = {}
		self.text = text
		self.words = []

	def add_rule(self, key):
		if key == "NER-Month":
			t = (r"((3[01]|[12][0-9]|[1-9])\s+)?(?:" + Util.to_rgx(self.dic[key]) + r")\s+\d+", "NER-Date")
			NER.RULES.append(t);

		t = (r"(?:" + Util.to_rgx(self.dic[key]) + r")", key)
		NER.RULES.append(t)

	def create(self, model_filenames):
		# Pour tous les fichiers sauf le dernier
		for filename in model_filenames[:-1]:
			d = ""
			d += Util.read_file(filename)
			lines = d.splitlines()
			self.dic[lines[0]] = lines[1:]

		# Le dernier fichier est traité différemment
		for line in Util.read_file(model_filenames.pop()).splitlines():
			(key, value) = line.split(" : ")
			value = value.split(", ")
			self.dic[key] = value


		self.add_rule("NER-Day")
		# self.add_rule("NER-Person")
		# self.add_rule("NER-Loc")
		self.add_rule("NER-Movie")
		self.add_rule("NER-Month")
		self.add_rule("NER-Sugg")

	def match(self):
		for rule in NER.RULES:
			for m in re.finditer(rule[0], self.text):
				self.words.append(tuple((m.group(), rule[1], m.start(), m.end())))

	def get_words(self):
		return self.words

	def rm_duplicate(self):
		# TODO with while loop
		lst_fw = []
		for i in range(0, len(self.words)):
			start = self.words[i][2]
			end = self.words[i][3]
			founded = i
			for j in range(i, len(self.words)):
				if j != i and self.words[j][2] == start and self.words[j][3] > end:
					founded = j
					end = self.words[j][3]
			lst_fw.append(self.words[founded])
		lst_fw = sorted(list(set(lst_fw)), key=lambda x: x[2])

		lst_back = []
		for i in range(0, len(lst_fw)):
			start = lst_fw[i][2]
			end = lst_fw[i][3]
			founded = i
			for j in range(i, len(lst_fw)):
				if j != i and lst_fw[j][3] == end and lst_fw[j][2] < start:
					founded = j
					start = lst_fw[j][2]
			lst_back.append(lst_fw[founded])
		lst_back = sorted(list(set(lst_back)), key=lambda x: x[2])

		lst_eq = []
		it = 0;
		while it < len(lst_back):
			start = lst_back[it][2]
			end = lst_back[it][3]
			founded = it
			for j in range(it, len(lst_back)):
				it += 1
				if j != it and lst_back[j][3] == end and lst_back[j][2] == start:
					founded = j
					start = lst_back[j][2]
					end = lst_back[j][3]
					continue
				break
			lst_eq.append(lst_back[founded])
		lst_eq = sorted(list(set(lst_eq)), key=lambda x: x[2])

		"""
		seen = set() 
		lst_eq = [(a, b, c, d) for a, b, c, d in lst_back 
		          if not a in seen or seen.add(a)]
  		"""

		self.words = lst_eq


	def add_to_dic(self):
		for w in self.words:
			if w[1] == "NER-Obj":
				self.dic["NER-Sugg"].append(w[0])

		dic_ = {}
		dic_["NER-Sugg"] = self.dic["NER-Sugg"]
		words_sugg = list(set(dic_["NER-Sugg"]))
		dic_["NER-Sugg"] = words_sugg
		Util.write_file("data/sugg.txt", Util.dic_to_text(dic_))


