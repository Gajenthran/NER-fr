from nltk.chunk import RegexpParser
import re

class Parser:
	"""
		Classe s'occupant du parsing du texte en créant un ensemble de règles grammaticales afin d'obtenir
		une syntaxe contenant une NE.
	"""
	# Grammaire réalisée avec StanfordPOSTagger
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

		NER-Time:
			{<Ltime>}

		NER-Number: 
			{<Lnumber>+}

		NER-Money:
			{<NER-Number> <NC|N>* <Lmoney|LmoneyM>}

		NER-Pourcent:
			{<NER-Number> <NC|N>* <Lpourcent>}

		NER-Time:
			{<NER-Number> <Lutime>}
			{<Ltime>}

		NER-Unit:
			{<NER-Number> <Lunit>}
			{<Lunit>}

		NER-Person:
			{<Lperson|LpersonM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <Lperson|LpersonM> <PUNC> <N|Lobj|NPP>+}
			{<Lperson|LpersonM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lperson|LpersonM> <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lcom>? <DET>* <Lperson|LpersonM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)*}
			{<Lperson|LpersonM> <PUNC> <N|Lobj|NPP>+}
		
		NER-Loc:
			{<NER-Number> <Lloc> <P>* <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lloc|LlocM> <P>* <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}

		NER-Org:
			{<Lorg|LorgM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lcom>? <DET>* <Lorg|LorgM> <ADJ>* (<P> <DET>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <CC>* <Lcom>*)*}
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

	# Grammaire réalisée sans StanfordPOSTagger
	GRAMMAR_OWN_TAG = """
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

		NER-Time:
			{<Ltime>}

		NER-Number: 
			{<Lnumber>+}

		NER-Money:
			{<NER-Number> <Lmoney|LmoneyM>}

		NER-Pourcent:
			{<NER-Number> <Lpourcent>}

		NER-Time:
			{<NER-Number> <Lutime>}
			{<Ltime>}

		NER-Unit:
			{<NER-Number> <Lunit>}
			{<Lunit>}

		NER-Person:
			{<Lperson|LpersonM> (<Lprep> <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <Lcc>* <Lcom>*)* <Lcom>? <Lperson|LpersonM> <PUNC> <N|Lobj|NPP>+}
			{<Lperson|LpersonM> (<Lprep> <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <Lcc>* <Lcom>*)* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lperson|LpersonM> <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lcom>? <DET>* <Lperson|LpersonM> (<Lprep> <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <Lcc>* <Lcom>*)*}
			{<Lperson|LpersonM> <PUNC> <N|Lobj|NPP>+}
		
		NER-Loc:
			{<NER-Number> <Lloc> <Lprep>* <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lloc|LlocM> <Lprep>* <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}

		NER-Org:
			{<Lorg|LorgM> ((<Lprep>|<Ldet>)* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <Lcc>* <Lcom>*)* <Lcom>? <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lcom>? <Ldet>* <Lorg|LorgM> (<Lprep> <Ldet>* <Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM|NER-Loc>+ <Lcc>* <Lcom>*)*}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+ <Lorg|LorgM>}

		NER-Date:
			{<NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
			{<NER-Number> <NER-Month|NC> <NER-Number>}
			{<NER-Number> <NER-Month>}
			{<Ldate>}

		NER-Obj:
			{<Lobj|NPP>+ <NER-Number>}
			{<Lobj|NPP|LdayM|LmonthM|LlocM|LpersonM|LorgM|LmoneyM>+}
	"""

	def __init__(self, tokens, own_tag=False):
		self.tokens = tokens
		self.tagged_nodes = []
		self.own_tag = own_tag

	def parse(self):
		"""
			Parse le texte tokenisé à l'aide de notre grammaire créé pour récupérer les groupes de mots 
			contenant une NE.
		"""
		if self.own_tag:
			rp = RegexpParser(Parser.GRAMMAR_OWN_TAG)
		else:
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
