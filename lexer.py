from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import WhitespaceTokenizer
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
	LEXEMES = r"quelqu'un|aujourd'hui|prud'hom\w+|c'est-à-dire|Prud'hom\w+|Quelqu'un|Aujourd'hui|C'est-à-dire|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|[0-9]+\/[0-9]+\/[0-9]+|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´’`]|\$[\d\.]+|\w+|€|\$|£"

	# Ensemble des types des mots
	MAJ_MONTH_TAG = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Août|Septembre|Octobre|Novembre|Decembre|Décembre)$"
	MONTH_TAG = r"^(?:janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|août|septembre|octobre|novembre|decembre|décembre)$"
	MAJ_DAY_TAG = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)$"
	DAY_TAG = r"^(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)$"
	MAJ_MONEY_TAG = r"^(?:EUR|USD|GBP)$"
	MONEY_TAG = r"^(?:€|\$|£|euros|euro|dollars|dollar|EUR|USD|yen|yens|dinar|dinars|GBP|francs|franc)$"
	NUMBER_TAG = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingts|vingt et un|trente|trente et un|quarante et un|quarante|cinquante et un|cinquante|soixante et un|soixante|soixante et onze|cent|cents|mille|milles|millions|million|milliard|milliards|billion|billions)"
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

	def __init__(self, text):
		self.text = text
		self.tagged_tokens = []

	def add_rules(self, filename):
		"""
			Ajouter de nouvelles règles pour renforcer l'analyse lexicale

			:param nom du fichier contenant les mots
			:return expression régulière
		"""
		file = Util.read_file(filename)
		d = file.split();
		d = Util.to_rgx_lex(d)
		return d

	def lex(self):
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
		
		for m in re.finditer(r"\.|!|\?|\.\.\.|:|;|…|»|«|—|–|-", self.text):
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


	def get_tokenized_text(self):
		"""
			Récupére tous les tokens/lexèmes du texte.

			:return les tokens du texte
		"""
		return self.tagged_tokens