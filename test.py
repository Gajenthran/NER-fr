import os
import nltk
import re
from util import Util
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
import nltk, nltk.data, nltk.tag
from nltk import FreqDist
from tagger import Tagger
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.chunk import RegexpParser
from nltk.tokenize import WhitespaceTokenizer
from lexer import Lexer
from parser import Parser
from sem import SEM

jar = 'stanford-postagger/stanford-postagger-3.9.2.jar'
model = 'stanford-postagger/models/french.tagger'
# java_path = "C:/Program Files/Java/jdk1.8.0_121/bin/java.exe"
# os.environ['JAVAHOME'] = java_path

# guillemet
# accent
# euros
# time
# pourcentages
# 21/2/2010
# n'golo Kanté
# & °
# cardinalité
# romain



MONTH = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre|Décembre|janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre|décembre)$"
DAY = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)$"
PERSON = r"^(?:Président|roi|Roi|Reine|reine|président|Data scientist|Statisticien|Analyste|Médecin|Échographiste|Mathématicien|Ingénieur|Pathologiste|Actuaire|Ergothérapeute|Directeur|Hygiéniste|Diététicien|Météorologue|Administrateur|Ophtalmologue|Thérapeute|Physicien|Chiropracteur|Technicien|Économiste|Responsable|Développeur|Pharmacien|Interprète|Traducteur|Rédacteur|Expert-Comptable|Agent|Juriste|Biologiste|Professeur|Podologue|Opticien|Libraire|Géologue|Orthodontiste|Écologiste|Manager|Artiste multimédia|Psychiatre|Dentiste|Vétérinaire|Psychologue|Programmeur|Conseiller d’orientation|Coiffeur|Historien|Assistant|Physiologiste|Consultant|Juge|Directeur|Principal|Zoologiste|Conservateur de musée|Dessinateur|Sociologue|Bijoutier|Physicien|Assureur|Comptable|Aide-enseignant|Dermatologue|Assistant|Dactylographe|Électricien|Assistant|Inspecteur|Chirurgien|Sténographe|Scientifique|Recruteur|Secrétaire médicale|Community Manager|Grossiste|Machiniste|Religieux|Monsieur|M|Mister|Mr|Messieurs|MM|Madame|Mme|Mesdames|Mmes|Mademoiselle|Mlle|Mesdemoiselles|Mlles|Veuve|Vve|Docteur|Dr|Docteurs|Drs|Maître|Maîtres|Professeur|Pr|Professeurs|Prs|Auditeur|Aud|Ingénieur Civil|Ir|Ingénieur Industriel|Ing|Duc|Duchesse|Marquis|Marquise|Comte|Cte|Comtesse|Ctesse|Vicomte|Vte|Vicomtesse|Vtesse|Baron|Bon|Baronne|Bonne|Seigneur|Sgr|Dame|Écuyer|Ec|Messire|Sir|Lady|Lord|Émir|Émira|Chérif|Chérifa|Cheikh|Cheykha|Bey|Calife|Hadjib|Nizam|Pervane|Sultan|Vizir|Râja|Rani|Malik|Shah|Padishah|Dom|Don|Père|P|Monsieur l'Abbé|Monsieur le Curé|Mère|M|Frère|Fr|Sœur|Sr|Révérend|Monseigneur|Mgr|Messeigneurs|Mgrs|Rabbin)$"
LOC = r"^(?:Aéroport|aéroport|Vallée|Université|université|sud|nord|ouest|Sud|Ouest|Nord|Rue|rue|Pays|Région|région|Cote|Côte|Place|Avenue|Passage|Pays|Allée|Boulevard|boulevard|Carrefour|carrefour|chemin|Chemin|Cité|cité|Cour|Esplanade|Impasse|Gallerie|gallerie|Pont|pont|Quai|quai|Route|route|Square|square|Terrasse|terrasse|Villa|ville)$"
MONEY = r"^(?:€|\$|£|euros|euro|dollars|dollar|EUR|USD|yen|yens|dinar|dinars|GBP|francs|franc)$"
NUMBER = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingts|vingt et un|trente|trente et un|quarante et un|quarante|cinquante et un|cinquante|soixante et un|soixante|soixante et onze|cent|cents|mille|milles|millions|million|milliard|milliards|billion|billions)"
ORG = r"^(?:entreprise|\.inc|\.Inc|Agence|agence|groupe|Groupe|organisation|Organisation|Société|société)$"
PUNC = r"^(?:…|»|«|—|–|-|’|ʼ|')$"
RULES = [
	# (r'(0[0-9]|1[0-9]|2[0-3]|[0-9])(?:\s*h\s*|\s*:\s*)[0-5][0-9]', "NER-Time"),
	# (r'(\d+)\s*(?:heures|heure|h|minute\w*|min|\w*seconde\w*|sec)', "NER-Time"),

	(r"^(?:|,|;|:)$", "Lcom"),

	(PERSON, "Lperson"),

	(LOC, "Lloc"),

	(ORG, "Lorg"),

	(MONEY, "Lmoney"),

	(MONTH, "NER-Month"),
	# (r"((3[01]|[12][0-9]|[1-9])\s+)?(?:" + lst_exprs(trained_dic["NER-Month"]) + r")\s+\d+", "NER-Date"),

	(DAY, "NER-Day"),

	(r"^" + NUMBER + r"-" + NUMBER + r"$", "Lnumber"), # en lettre

	(r"^" + NUMBER + r"$", "Lnumber"), # en lettre

	# (r"(?:" + lst_exprs(trained_dic["NER-Day"]) + r")", "NER-Day"),

	(r"^[A-Z](?:\.[A-Z]){1,7}$", "NER-Acronym"),

	(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "NER-Mail"),

	(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', "NER-Date"),

	(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),

	(r"^(?:-|\+)?\d*(?:\.|,)?\d+$", "Lnumber"), # en lettre

	# (NUMBER, "Lnumber"),

	(r"^[A-Z]\w*-\w\w*$", "NER-Obj"),

	(r"^[a-z_]+[A-Z0-9_][a-z0-9_]*$", "NER-Obj"),
	# (r"[a-z]+(?:-|\.|'|’)?[A-Z0-9]\w*", "NER-lowerCamelCase"),

	(r'^[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*$', "NER-Obj"),
	# (r'^[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*', "NER-upperCamelCase"),

	(r"^[A-Z]\w*$", "NER-Obj"),
	# (r"(?<!" + PONCT + r"\s)(?!^)\b([A-Z]\w*(?:(?:\s|-|\.|'|’)[A-Z]\w*)*)", "NER-Obj"),

	(PUNC, "PUNC"),

	# (r"(?:" + lst_exprs(trained_dic["NER-Person"]) + r")", "NER-Person"),
	# (r"(?:" + lst_exprs(trained_dic["NER-Sugg"]) + r")", "NER-Sugg"),
]

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

ex = "Le Président François Hollande n'est plus président mais la France règne toujours en Maitre."
ex = read_file("toto.txt")

ex = Util.transform_text(ex)
lexer = Lexer(ex)
lexer.lex()
parser = Parser(lexer.get_tokens())
parser.parse()

sem = SEM(ex, parser.get_tagged_tokens())
sem.gen_models(["data/location.txt", "data/person.txt"])
sem.apply()
tagger = Tagger(sem.get_ner(), ex);
tagger.tag("fifi.txt")
exit()

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')
reg_words = r"Quelqu'un|Aujourd'hui|c'est-à-dire|[0-9]+\/[0-9]+\/[0-9]+|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´`]|\$[\d\.]+|quelqu'un|aujourd'hui|prud'hom\w+|\w+|\S+"
# reg_words += u"|\w\u2019"
# reg_words += u"|\w+|[^\w\s]"

tok = RegexpTokenizer(reg_words)
tokenized_ex = tok.tokenize(ex)
res = pos_tagger.tag(tokenized_ex)

print(res)
for i in range(0, len(res)):
	for rule in RULES:
		for m in re.finditer(rule[0], res[i][0]):
			if i == 0 and rule[1] == "NER-Obj" or i > 0 and res[i-1][1] == 'PUNC' and rule[1] == "NER-Obj":
				continue
			if res[i][1].startswith("NER-") or res[i][1].startswith("L"):
				continue
			# tuple with position
			res[i] = tuple((m.group(), rule[1]))

print(res)

# Le président de la Cote d'Ivoire
# Le medecin allemand Viknesh
grammar = r"""
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

cp = RegexpParser(grammar)
tree = cp.parse(res)
print(tree)

words = []
for subtree in tree.subtrees():
	if subtree.label() == "S":
		continue
	words.append(tuple((subtree.label(), subtree.leaves())))

dic = {}

def create(model_filenames):
	# Pour tous les fichiers sauf le dernier
	for filename in model_filenames:
		print(filename)
		d = ""
		d += Util.read_file(filename)
		lines = d.splitlines()
		dic[lines[0]] = lines[1:]

create(["data/location.txt", "data/person.txt"])
# print(dic)

rl = []

rl.append(tuple(("NER-Loc", r"(?:" + Util.to_rgx(dic["NER-Loc"])+ r")")))
rl.append(tuple(("NER-Person", r"(?:" + Util.to_rgx(dic["NER-Person"])+ r")")))

w = []
for iw in range(0, len(words)):
	lst = [i[0] for i in words[iw][1]]
	lst = r' '.join(lst)
	# words[iw][1] = lst
	w.append([lst, words[iw][0]])


for iw in range(0, len(w)):
	for r in rl:
		if w[iw][0] == "NER-Obj":
			for m in re.finditer(r[1], w[iw][1]):
				w[iw][0] = r[0]

for words in w:
	print(words)

print()
lst = []
for words in w:
	for m in re.finditer(r"\b" + words[0] + r"\b", ex):
		lst.append(tuple((m.group(), words[1], m.start(), m.end())))

lst = sorted(list(set(lst)), key=lambda x: x[2])
print(lst)
tagger = Tagger(lst, ex);
tagger.tag("fifi.txt")
