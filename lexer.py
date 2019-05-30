from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
import nltk
from util import Util
import re

class Lexer:
	"""
		Classe qui produira l'analyse lexicale du texte afin de permettre l'analyse 
		syntaxique. L'analyse lexicale va permettre de couper le texte en lexèmes ("mot"),
		en leur attribuant des types. Pour cela nous nous aiderons du StanfordPOSTagger.
	"""

	JAR = 'stanford-postagger/stanford-postagger-3.9.2.jar'
	MODEL = 'stanford-postagger/models/french.tagger'

	# Expression régulière permettant de couper le texte en lexème
	LEXEMES = r"quelqu'un|aujourd'hui|prud'hom\w+|c'est-à-dire|Prud'hom\w+|Quelqu'un|Aujourd'hui|C'est-à-dire|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|[0-9]+\/[0-9]+\/[0-9]+|[0-9]+:[0-9]+|[0-9]+h[0-9]+min|[0-9]+h[0-9]+|[0-9]+min|[0-9]+s|[0-9]+sec|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´’`]|\$[\d\.]+|\w+|€|\$|£|%"

	# Ensemble des types des mots
	MAJ_MONTH_TAG = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Août|Septembre|Octobre|Novembre|Decembre|Décembre)$"
	MONTH_TAG = r"^(?:janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|août|septembre|octobre|novembre|decembre|décembre)$"
	MAJ_DAY_TAG = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)$"
	DAY_TAG = r"^(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)$"
	MAJ_MONEY_TAG = r"^(?:EUR|USD|GBP)$"
	MONEY_TAG = r"^(?:€|\$|£|euros|euro|centime|centimes|dollars|dollar|EUR|USD|yen|yens|dinar|dinars|GBP|francs|franc)$"
	NUMBER_TAG = r"^(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingts|vingt et un|trente|trente et un|quarante et un|quarante|cinquante et un|cinquante|soixante et un|soixante|soixante et onze|cent|cents|mille|milles|millions|million|milliard|milliards|billion|billions)$"
	POURCENTAGE_TAG = r"^(?:%|pourcent)$"
	UNIT_TAG = r"^[0-9]*(?:mètre|milimètre|centimètre|décimètre|décamètre|hectomètre|kilomètre|mètres|milimètres|centimètres|décimètres|décamètres|hectomètres|kilomètres|m|mm|cm|dm|dam|hm|km|kilogramme|hectogramme|décagramme|décigramme|gramme|centigramme|milligramme|kilogrammes|kilo|hectogrammes|décagrammes|décigrammes|grammes|centigrammes|milligrammes|kg|hg|dag|dg|cg|mg|g|mol|Hz|hz|Hertz|W|Watt|Watts|Volt|Volts|volts|volt|watt|watts|hertz)$"
	TIME_TAG = r"^(?:min|h|sec|s|minutes|minute|seconde|secondes|heures|heure)$"
	PUNC_TAG = r"^(?:…|»|«|—|–|-|’|ʼ|')$"

	# Ensemble des règles pour attribuer les types des mots
	RULES_TAG = [
		(r"^(?:|,|;|:)$", "Lcom"),
		(MONEY_TAG, "Lmoney"),
		(MAJ_MONEY_TAG, "LmoneyM"),
		(MONTH_TAG, "Lmonth"),
		(MAJ_MONTH_TAG, "LmonthM"),
		(DAY_TAG, "Lday"),
		(MAJ_DAY_TAG, "LdayM"),
		(POURCENTAGE_TAG, "Lpourcent"),
		(TIME_TAG, "Lutime"),
		(UNIT_TAG, "Lunit"),
		(r"^(?:[0-9]+:[0-9]+|[0-9]+h[0-9]+min|[0-9]+h[0-9]+|[0-9]+min|[0-9]+s|[0-9]+sec)$", "Ltime"),
		(r"^" + NUMBER_TAG + r"-" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^[A-ZÀÁÂÆÇÈÉÊËÌÍÎÏÑÒÓÔŒÙÚÛÜÝŸß](?:\.[A-ZÀÁÂÆÇÈÉÊËÌÍÎÏÑÒÓÔŒÙÚÛÜÝŸß]){1,7}$", "Lacronym"),
		(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "Lmail"),
		(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', "Ldate"),
		(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "Lurl"),
		(r"^(?:-|\+)?\d*(?:\.|,)?\d+$", "Lnumber"), # en lettre
		(r"^[A-ZÀÁÂÆÇÈÉÊËÌÍÎÏÑÒÓÔŒÙÚÛÜÝŸß]\w*-\w\w*$", "Lobj"),
		(r"^[a-zàáâæçèéêëìíîïñòóôœùúûüýÿß_]+[A-Z0-9_][a-z0-9_]*$", "Lobj"),
		(r'^[A-Zß]([A-Z0-9]*[a-z][a-z0-9]*[A-ZÀÁÂÆÇÈÉÊËÌÍÎÏÑÒÓÔŒÙÚÛÜÝŸß]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*$', "Lobj"),
		(r"^[A-ZÀÁÂÆÇÈÉÊËÌÍÎÏÑÒÓÔŒÙÚÛÜÝŸß]\w*$", "Lobj"),
		(PUNC_TAG, "PUNC"),
	]

	def __init__(self, text, own_tag=False):
		self.text = text
		self.tagged_tokens = []
		self.own_tag = own_tag

	def add_rules(self, filename):
		"""
			Ajouter de nouvelles règles pour renforcer l'analyse lexicale

			:param nom du fichier contenant les mots
			:return expression régulière
		"""
		file = Util.read_file(filename)
		d = file.split()
		d = Util.to_rgx_lex(d)
		return d

	def tokenize_own_tag(self):
		"""
			Analyse le texte lexicalement, à l'aide des règles et des expressions régulières définies.
			On obtiendra à la fin un tableau de tous les tokens/lexèmes du texte sans l'aide de
			StanfordPOSTagger.
		"""
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/fonction.txt"), "Lperson")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/location.txt"), "Lloc")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/organisation.txt"), "Lorg")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/fonction_maj.txt"), "LpersonM")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/location_maj.txt"), "LlocM")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/organisation_maj.txt"), "LorgM")))

		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/conjonction.txt"), "Lcc")))
		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/preposition.txt"), "Lprep")))
		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/determinant.txt"), "Ldet")))
		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/adverbe.txt"), "Ladv")))
		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/pronom.txt"), "Lpronom")))
		Lexer.RULES_TAG.append(tuple((self.add_rules("tag/subordination.txt"), "Lsub")))

		tokenizer = RegexpTokenizer(Lexer.LEXEMES)
		tokens = tokenizer.tokenize(self.text)

		begin = 0
		for i in range(0, len(tokens)):
			for m in re.finditer(tokens[i], self.text):
				if(m.end() > begin):
					tokens[i] = tuple((tokens[i], m.start(), m.end()))
					begin = m.end()
					break


		for i in range(0, len(tokens)):
			if len(tokens[i]) != 3:
				tokens[i] = 0

		tokens = Util.rm_duplicate(tokens)
		for m in re.finditer(r"\.|!|\?|\.\.\.|:|,|;|…|»|«|—|–|-", self.text):
			if m.group() == r"," or m.group() == r":" or m.group() == r";":
				self.tagged_tokens.append([m.group(), "Lcom", m.start(), m.end()])
			else:
				self.tagged_tokens.append([m.group(), "PUNC", m.start(), m.end()])

		for i in range(0, len(tokens)):
			find = False
			for rt in Lexer.RULES_TAG:
				for m in re.finditer(rt[0], tokens[i][0]):
					find = True
					if i == 0:
						self.tagged_tokens.append([tokens[i][0], "None", tokens[i][1], tokens[i][2]])
						continue
					if len(self.tagged_tokens) != 0 and m.group() == self.tagged_tokens[-1][0] and tokens[i][1] == self.tagged_tokens[-1][2]:
						continue
					self.tagged_tokens.append([m.group(), rt[1], tokens[i][1], tokens[i][2]])
			if not(find):
				self.tagged_tokens.append([tokens[i][0], "None", tokens[i][1], tokens[i][2]])
		self.tagged_tokens = sorted(self.tagged_tokens, key=lambda x: x[2])

		for i in range(0, len(self.tagged_tokens)):
			if(i > 0 and self.tagged_tokens[i-1][1] == "PUNC"):
				find = False
				for j in range(1, len(self.tagged_tokens)):
					if (self.tagged_tokens[j-1][1] != "PUNC" and self.tagged_tokens[j][1] == "Lobj") and self.tagged_tokens[i][0] == self.tagged_tokens[j][0] and self.tagged_tokens[i][2] != self.tagged_tokens[j][2]:
						find = True
						break
				if not(find) and self.tagged_tokens[i][1] == "Lobj":
					self.tagged_tokens[i][1] = "None"

		self.tagged_tokens = [tuple(l) for l in self.tagged_tokens]
		print(self.tagged_tokens)

	def tokenize(self):
		"""
			Analyse le texte lexicalement, à l'aide des règles et des expressions régulières définies.
			On obtiendra à la fin un tableau de tous les tokens/lexèmes du texte.
		"""
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/fonction.txt"), "Lperson")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/location.txt"), "Lloc")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/organisation.txt"), "Lorg")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/fonction_maj.txt"), "LpersonM")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/location_maj.txt"), "LlocM")))
		Lexer.RULES_TAG.insert(0, tuple((self.add_rules("tag/organisation_maj.txt"), "LorgM")))

		pos_tagger = StanfordPOSTagger(Lexer.MODEL, Lexer.JAR, encoding='utf8')
		tokenizer = RegexpTokenizer(Lexer.LEXEMES)
		self.tagged_tokens = pos_tagger.tag(tokenizer.tokenize(self.text))

		begin = 0
		for i in range(0, len(self.tagged_tokens)):
			for m in re.finditer(self.tagged_tokens[i][0], self.text):
				if(m.end() > begin):
					self.tagged_tokens[i] += tuple((m.start(), m.end()))
					begin = m.end()
					break

		for i in range(0, len(self.tagged_tokens)):
			if len(self.tagged_tokens[i]) != 4:
				self.tagged_tokens[i] = 0

		self.tagged_tokens = Util.rm_duplicate(self.tagged_tokens)
		
		for m in re.finditer(r"\.|!|\?|\.\.\.|:|,|;|…|»|«|—|–|-", self.text):
			self.tagged_tokens.append(tuple((m.group(), "PUNC", m.start(), m.end())))

		self.tagged_tokens = sorted(self.tagged_tokens, key=lambda x: x[2])
		for i in range(0, len(self.tagged_tokens)):
			for rt in Lexer.RULES_TAG:
				for m in re.finditer(rt[0], self.tagged_tokens[i][0]):
					if (i == 0 and rt[1] == "Lobj") or (i > 0 and self.tagged_tokens[i-1][1] == "PUNC" and rt[1] == "Lobj"):
						continue
					if self.tagged_tokens[i][1].startswith("L"):
						continue
					self.tagged_tokens[i] = tuple((m.group(), rt[1], self.tagged_tokens[i][2], self.tagged_tokens[i][3]))
		print(self.tagged_tokens)

	def lex(self):
		"""
			Analyse le texte lexicalement, avec ou sans le StanfordPOSTagger selon les options.
		"""
		if self.own_tag:
			self.tokenize_own_tag()
		else:
			self.tokenize()

	def get_tokenized_text(self):
		"""
			Récupére tous les tokens/lexèmes du texte.

			:return les tokens du texte
		"""
		return self.tagged_tokens