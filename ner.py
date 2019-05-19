from util import Util
import re

class NER:
	def __init__(self, text, tagged_nodes):
		self.tagged_nodes = tagged_nodes
		self.text = text
		self.ner_obj = []
		self.dic = []

	def check(self):
		"""
			Vérifie si les NE sont sémantiquement correctes, en vérifiant le contenu de chaque
			élément et leurs liaisons avec les autres.
		"""
		for i in range(0, len(self.tagged_nodes)):
			if self.tagged_nodes[i][0] == "NER-Date" and not(self.check_date(i)):
				self.tagged_nodes[i] = 0
			# if self.tagged_nodes[i][0] == "NER-Loc":
			#  	self.tagged_nodes[i][1] = [tuple((self.tagged_nodes[i][1][-1][0], "NER-Loc"))]
			#  	self.tagged_nodes[i][0] = "NER-Loc"
		Util.rm_duplicate(self.tagged_nodes)

	def gen_models(self, model_filenames):
		"""
			Génère les modèles afin d'avoir une précision plus accrue sur le type des entités nommées.
			On perdra en temps mais on gagnera en précision.
		"""
		models = {}
		for filename in model_filenames:
			d = ""
			d += Util.read_file(filename)
			lines = d.splitlines()
			models[lines[0]] = lines[1:]

		for key in models:
			self.dic.append(tuple((key, r"(?:" + Util.to_rgx(models[key])+ r")")))

	def check_date(self, index):
		"""
			Vérifie le contenu de la date en vérifiant si la valeur représentant le jour
			est compris entre 1 e 31, et l'année correspond bien à une valeur positif
		"""
		day = False
		checked = True
		for tag in self.tagged_nodes[index][1]:
			if day == True and tag[1] == "Lnumber" and tag[0].isnumeric():
				if int(tag[0]) > 0:
					break
				else:
					checked = False
					break
			if tag[1] == "Lnumber" and tag[0].isnumeric():
				if 1 < int(tag[0]) < 31:
					day = True
				else:
					checked = False
					break
		return checked

	def create_ner(self):
		"""
			Crée à partir de l'AST obtenu par le Parser, la liste des entités nommées qui sera
			représentée sous la forme de pair avec 1. l'expression et 2. le type de l'expression.
		"""
		for i in range(0, len(self.tagged_nodes)):
			lst = [g[0] for g in self.tagged_nodes[i][1]]
			lst = r" ".join(lst)
			self.ner_obj.append([lst, self.tagged_nodes[i][0]])


	def use_models(self):
		"""
			Utilise les modèles afin d'avoir une précision plus accrue sur le type des entités nommées.
			On perdra en temps mais on gagnera en précision.
		"""
		for i in range(0, len(self.ner_obj)):
			for d in self.dic:
				if self.ner_obj[i][1] == "NER-Obj":
					for m in re.finditer(
						d[1], self.ner_obj[i][0]
					):
						self.ner_obj[i][1] = d[0]


	def filter_ner(self):
		"""
			Filtre les NE afin d'obtenir l'emplacement des NE et retirer les doublons.
		"""
		lst = []
		for ner in self.ner_obj:
			for m in re.finditer(r"\b" + ner[0] + r"\b", self.text):
				lst.append(tuple((m.group(), ner[1], m.start(), m.end())))
		# lst = Util.sort_ner(lst)
		lst = sorted(list(set(lst)), key=lambda x: x[2])
		# lst = Util.prioritize_obj(lst)
		self.ner_obj = lst


	def apply(self):
		"""
			Fonction principale de la classe qui servira à vérifier la sémantique du texte, à créer
			les NE, à utiliser les modèle et enfin à filter les NE.
		"""

		self.check()
		self.create_ner()
		self.use_models()
		self.filter_ner()
		print(self.ner_obj)


	def get_ner(self):
		"""
			Récupère les NE.

			:return liste de NE.
		"""
		return self.ner_obj