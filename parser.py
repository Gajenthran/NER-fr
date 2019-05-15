from nltk.chunk import RegexpParser
import re

class Parser:
	GRAMMAR = """
		NER-Money:
			{<NER-Number> <NC|N>* <Lmoney>}

		NER-Month:
			{<Lmonth>}

		NER-Day:
			{<Lday>}

		NER-Acronym:
			{<Lacronym>}

		NER-URL:
			{<Lurl>}

		NER-Mail:
			{<Lmail>}

		NER-Number: 
			{<Lnumber>+}

		NER-Obj:
			{<Lobj|NPP>+ <NER-Number>}
			{<Lobj|NPP>+}

		NER-Loc:
			{<NER-Number> <Lloc> <P>* <DET>* <NER-Obj>}
			{<Lloc> <P>* <DET>* <NER-Obj>}

		NER-Person:
			{<DET>* <ADJ>* <Lperson> <ADJ>* (<P> <DET>* <NER-Obj|NER-Loc>+ <CC>* <Lcom>*)* <ADJ>* <Lcom>? <NER-Obj>}
			{<DET>* <ADJ>* <Lperson> <ADJ>* <Lcom>? <NER-Obj>}
		
		NER-Org:
			{<Lorg> <P>* <NER-Obj>}
			{<NER-Obj> <Lorg>}

		NER-Date:
			{<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
			{<DET>? <NER-Number> <NER-Month|NC> <NER-Number>}
			{<DET>? <NER-Number> <NER-Month>}
			{<Ldate>}
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
