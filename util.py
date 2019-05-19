class Util:
	"""
		Classe utilitaire qui regroupera l'ensemble des fonctions utiles à
		notre analyse textuelle mais qui n'a pas de lien direct avec.
	"""
	def __init__(self):
		pass

	@staticmethod
	def read_file(filename):
		"""
			Lire un fichier donné en paramètre.

			:param filename: nom du fichier
			:return le contenu du fichier sous forme de string
		"""
		with open(filename, 'r') as file:
			data = file.read()
		return data

	@staticmethod
	def text_to_dic(text):
		"""
			Transforme le texte sous forme de dictionnaire en considérant 
			la première ligne du texte en tant que clé et le reste comme 
			valeur.

			:param text: texte
			:return un dictionnaire de la forme (key=première ligne, val=reste)
		"""
		dic = {}
		for line in text.splitlines():
			(key, value) = line.split(" : ")
			value = value.split("\n")
			dic[key] = value
		return dic

	@staticmethod
	def dic_to_text(dic):
		"""
			Transforme le dictionnaire sous la forme d'un texte en considérant
			la clé du dictionnaire comme la première ligne du texte.

			:param dic: dictionnaire
			:return un texte
		"""
		text = ""
		for key, value in dic.items():
			text += key + "\n" + '\n'.join(value)
		return text

	@staticmethod
	def write_file(filename, data):
		"""
			Ecrit le contenu d'un texte dans un fichier.

			:param filename: nom du fichier
			:param data: contenu à mettre dans un fichier
		"""
		with open(filename, 'w') as file:
			file.write(data)


	@staticmethod
	def to_rgx(expressions):
		"""
			Transforme une liste de mots en expression régulière avec chaque mot
			de la liste séparé par des |.

			:param expressions liste de mots
			:return une expression régulière
		"""
		reg = r'';
		for expr in expressions:
			reg += r'\b(' + expr + r')\b|';
		reg = reg[:-1];
		return reg;

	@staticmethod
	def to_rgx_lex(expressions):
		"""
			Transforme une liste de mots en expression régulière avec chaque mot
			de la liste séparé par des | pour l'analyse lexicale.

			:param expressions liste de mots
			:return une expression régulière
		"""
		reg = r'^(?:';
		for expr in expressions:
			reg += expr +r'|';
		reg = reg[:-1];
		reg += r")$"
		return reg;

	@staticmethod
	def prioritize_obj(lst):
		"""
			Mettre toutes les entités nommées non reconnues à la fin
			de la liste.

			:param lst liste des entités nommées
			:return nouvelle liste filtrée avec les NE non reconnues à la fin
		"""
		i = 0
		length = len(lst)
		while i < length:
			j = i + 1
			if not(j < length): break
			if lst[j][1] != "NER-Obj":
				while j < length:
					if lst[j][2] == lst[i][2] and lst[j][3] == lst[i][3]:
						lst[i] = 0
					j += 1
			i += 1

		lst = Util.rm_duplicate(lst)
		return lst

	@staticmethod
	def rm_duplicate(lst):
		"""
			Supprimer les doublons de NE dans la liste.

			:param lst liste de NE
			:return nouvelle liste filtrée sans doublon
		"""
		i = 0
		n = 0
		length = len(lst)
		while i < length:
			if lst[i] == n:
				lst.remove(lst[i])
				length = length -1  
				continue
			i = i+1

		return lst

	@staticmethod
	def transform_text(text):
		"""
			Formater un texte afin de faciliter l'analyse lexicale.

			:param text: text
			:return texte formaté
		"""
		text = text.replace("(" , " ( ")
		text = text.replace(")" , " ) ")
		text = text.replace("{" , " { ")
		text = text.replace("}" , " } ")
		text = text.replace("\"", " \" ")
		text = text.replace("'", "' ")
		text = text.replace(", ", " , ")
		return text

	@staticmethod
	def detransform_text(text):
		"""
			Déformater un texte afin de faciliter le balisage du texte.

			:param text texte formaté
			:return texte déformaté
		"""
		text = text.replace("' "   , "'")
		text = text.replace(" , "  , ", ")
		text = text.replace(" ( " , "(")
		text = text.replace(" ) " , ")")
		text = text.replace(" { " , "{")
		text = text.replace(" } " , "}")
		text = text.replace(" \" ", "\"")
		return text	
