from nltk.chunk import RegexpParser
import re

class Parser:
	"""
		Classe s'occupant du parsing du texte en créant un ensemble de règles grammaticales afin d'obtenir
		une syntaxe contenant une NE.
	"""
	GRAMMAR = """
		NER-Month:
			{<Lmonth>|<LmonthM>}

		NER-Day:
			{<Lday>|<LdayM>}

		NER-Acronym:
			{<Lacronym>}

		NER-URL:
			{<Lurl>}

		NER-Mail:
			{<Lmail>}

		NER-Number: 
			{<Lnumber>+}

		NER-Money:
			{<NER-Number> <NC|N>* <Lmoney|LmoneyM>}

		NER-Person:
			{<Lperson|LpersonM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lperson|LpersonM> <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
		
		NER-Loc:
			{<NER-Number> <Lloc> <P>* <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lloc|LlocM> <P>* <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}

		NER-Org:
			{<Lorg|LorgM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lorg|LorgM>}

		NER-Date:
			{<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
			{<DET>? <NER-Number> <NER-Month|NC> <NER-Number>}
			{<DET>? <NER-Number> <NER-Month>}
			{<Ldate>}

		NER-Obj:
			{<Lobj|NPP>+ <NER-Number>}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
	"""

	def __init__(self, tokens):
		self.tokens = tokens
		self.tagged_nodes = []

	def parse(self):
		"""
			Parse le texte tokenisé à l'aide de notre grammaire créé pour récupérer les groupes de mots 
			contenant une NE.
		"""
		rp = RegexpParser(Parser.GRAMMAR)
		tree = rp.parse(self.tokens)

		for subtree in tree.subtrees():
			if subtree.label() == "S":
				continue
			self.tagged_nodes.append(
				[subtree.label(), subtree.leaves()]
			)
		print(self.tagged_nodes)

	"""
		Récupère le texte parsé.

		:return le texte parsé
	"""
	def get_parsed_text(self):
		return self.tagged_nodes
