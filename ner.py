from util import Util
import re

class NER:
	PONCT = r'(?:—|-|\.|!|\?|«|"|\')';
	RULES = [
		(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", "NER-Mail"),
		(r'(0[0-9]|1[0-9]|2[0-3]|[0-9])(?:\s*h\s*|\s*:\s*)[0-5][0-9]', "NER-Time"),
		(r'(\d+)\s*(?:heures|heure|h|minute\w*|min|\w*seconde\w*|sec)', "NER-Time"),
		(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),
		(r'([0-2][0-9]|(3)[0-1])(?:\/|-)(((0)[0-9])|((1)[0-2]))(?:\/|-)\d{4}', "NER-Date"),
		(r"(?:-|\+)?\d*(?:\.|,)?\d+", "NER-Number"), # en lettre
		(r"(?<!" + PONCT + r"\s)(?!^)\b([A-Z]\w*(?:(?:\s+|-|\.|'|’)[A-Z]\w*)*)", "NER-Obj"),
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

	def create(self, model_filenames):
		for filename in model_filenames:
			d = ""
			d += Util.read_file(filename)
			lines = d.splitlines()
			self.dic[lines[0]] = lines[1:]

	def match(self):
		for rule in NER.RULES:
			for m in re.finditer(rule[0], self.text):
				self.words.append(tuple((m.group(), rule[1], m.start(), m.end())))

	def get_words(self):
		return self.words

	def rm_duplicate(self):
		filtered_lst = []
		for i in range(0, len(self.words)):
			start = self.words[i][2];
			end = self.words[i][3];
			founded = i;
			for j in range(0, len(self.words)):
				if j != i and self.words[j][2] == start and self.words[j][3] > end:
					founded = j;
					end = self.words[j][3];
			filtered_lst.append(self.words[founded]);

		filtered_lst = sorted(list(set(filtered_lst)), key=lambda x: x[2])
		filtered_lst2 = []
		for i in range(0, len(filtered_lst)):
			start = filtered_lst[i][2];
			end = filtered_lst[i][3];
			founded = i;
			for j in range(0, len(filtered_lst)):
				if j != i and filtered_lst[j][3] == end and filtered_lst[j][2] > start:
					founded = j;
					start = filtered_lst[j][2]
			filtered_lst2.append(filtered_lst[founded])

		filtered_lst2 = sorted(list(set(filtered_lst2)), key=lambda x: x[2])
		self.words = filtered_lst2
