from nltk.chunk import RegexpParser
import re

class Parser:
	GRAMMAR = """
		NER-Obj: 
			{<NER-Obj|NPP>+}

		NER-Number: 
			{<Lnumber>+}

		Ploc:
			{<NER-Number> <Lloc> <P>* <DET>* <NER-Obj>}
			{<Lloc> <P>* <DET>* <NER-Obj>}

		Ppers:
			{<DET>* <ADJ>* <Lperson> <ADJ>* (<P> <DET>* <NPP|NC|N|NER-Obj|Ploc> <CC>* <Lcom>*)* <ADJ>* <Lcom>? <NER-Obj>}
			{<DET>* <ADJ>* <Lperson> <ADJ>* <Lcom>? <NER-Obj>}
		
		Porg:
			{<Lorg> <P>* <NER-Obj>}
			{<NER-Obj> <Lorg>}

		NER-Date:
			{<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
			{<DET>? <NER-Number> <NER-Month|NC> <NER-Number>}
			{<DET>? <NER-Number> <NER-Month>}

		NER-Money:
			{<NER-Number> <NC|N>* <Lmoney>}

		NER-Day:
			{<NER-Day>}

		NER-Month:
			{<NER-Month>}

		NER-Acronym:
			{<NER-Acronym>}

		NER-URL:
			{<NER-URL>}

		NER-Mail:
			{<NER-Mail>}
	"""

	def __init__(self, tokens):
		self.tokens = tokens
		self.tagged_tokens = []

	def parse(self):
		rp = RegexpParser(Parser.GRAMMAR)
		tree = rp.parse(self.tokens)

		for subtree in tree.subtrees():
			if subtree.label() == "S":
				continue
			self.tagged_tokens.append(
				[subtree.label(), subtree.leaves()]
			)

	def get_tagged_tokens(self):
		return self.tagged_tokens
