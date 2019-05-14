import os
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
import nltk, nltk.data, nltk.tag
from nltk import FreqDist
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.chunk import RegexpParser
from nltk.tokenize import WhitespaceTokenizer

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
PERSON = r"^(?:Président|président|Data scientist|Statisticien|Analyste|Médecin|Échographiste|Mathématicien|Ingénieur|Pathologiste|Actuaire|Ergothérapeute|Directeur|Hygiéniste|Diététicien|Météorologue|Administrateur|Ophtalmologue|Thérapeute|Physicien|Chiropracteur|Technicien|Économiste|Responsable|Développeur|Pharmacien|Interprète|Traducteur|Rédacteur|Expert-Comptable|Agent|Juriste|Biologiste|Professeur|Podologue|Opticien|Libraire|Géologue|Orthodontiste|Écologiste|Manager|Artiste multimédia|Psychiatre|Dentiste|Vétérinaire|Psychologue|Programmeur|Conseiller d’orientation|Coiffeur|Historien|Assistant|Physiologiste|Consultant|Juge|Directeur|Principal|Zoologiste|Conservateur de musée|Dessinateur|Sociologue|Bijoutier|Physicien|Assureur|Comptable|Aide-enseignant|Dermatologue|Assistant|Dactylographe|Électricien|Assistant|Inspecteur|Chirurgien|Sténographe|Scientifique|Recruteur|Secrétaire médicale|Community Manager|Grossiste|Machiniste|Religieux|Monsieur|M|Mister|Mr|Messieurs|MM|Madame|Mme|Mesdames|Mmes|Mademoiselle|Mlle|Mesdemoiselles|Mlles|Veuve|Vve|Docteur|Dr|Docteurs|Drs|Maître|Maîtres|Professeur|Pr|Professeurs|Prs|Auditeur|Aud|Ingénieur Civil|Ir|Ingénieur Industriel|Ing|Duc|Duchesse|Marquis|Marquise|Comte|Cte|Comtesse|Ctesse|Vicomte|Vte|Vicomtesse|Vtesse|Baron|Bon|Baronne|Bonne|Seigneur|Sgr|Dame|Écuyer|Ec|Messire|Sir|Lady|Lord|Émir|Émira|Chérif|Chérifa|Cheikh|Cheykha|Bey|Calife|Hadjib|Nizam|Pervane|Sultan|Vizir|Râja|Rani|Malik|Shah|Padishah|Dom|Don|Père|P|Monsieur l'Abbé|Monsieur le Curé|Mère|M|Frère|Fr|Sœur|Sr|Révérend|Monseigneur|Mgr|Messeigneurs|Mgrs|Rabbin)$"
LOC = r"^(?:Rue|rue|Pays|Région|région|Cote|Place|Avenue|Passage|Pays|Allée|Boulevard|boulevard|Carrefour|carrefour|chemin|Chemin|Cité|cité|Cour|Esplanade|Impasse|Gallerie|gallerie|Pont|pont|Quai|quai|Route|route|Square|square|Terrasse|terrasse|Villa|ville)$"
MONEY = r"^(?:€|\$|£|euros|euro|dollars|dollar|EUR|USD|yen|yens|dinar|dinars|GBP|francs|franc)$"
NUMBER = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingts|vingt et un|trente|trente et un|quarante et un|quarante|cinquante et un|cinquante|soixante et un|soixante|soixante et onze|cent|cents|mille|milles|millions|million|milliard|milliards|billion|billions)"
ORG = r"^(?:entreprise|\.inc|\.Inc|Agence|agence|groupe|Groupe|organisation|Organisation|Société|société)$"
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

	(NUMBER, "Lnumber"), # en lettre

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


	# (r"(?:" + lst_exprs(trained_dic["NER-Person"]) + r")", "NER-Person"),
	# (r"(?:" + lst_exprs(trained_dic["NER-Sugg"]) + r")", "NER-Sugg"),
]

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

ex = "L'Organisation des Nations Unies est un ensemble et deux pays fondée par N'Golo Kanté"
# ex = read_file("toto.txt")
ex = ex.replace("(", " ")
ex = ex.replace(")", " ")
ex = ex.replace("{", " ")
ex = ex.replace("}", " ")
ex = ex.replace("\"", " ")

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')
reg_words = r"Quelqu'un|Aujourd'hui|c'est-à-dire|[0-9]+\/[0-9]+\/[0-9]+|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´`]|\$[\d\.]+|quelqu'un|aujourd'hui|prud'hom\w+|\w+|\S+"
# reg_words += u"|\w\u2019"
# reg_words += u"|\w+|[^\w\s]"

tok = RegexpTokenizer(reg_words)
tokenized_ex = tok.tokenize(ex)
res = pos_tagger.tag(tokenized_ex)

for i in range(1, len(res)):
	if res[i-1][1] == 'PUNC' and res[i][0].isalpha():
		continue

	for rule in RULES:
		for m in re.finditer(rule[0], res[i][0]):
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
		{<DET>* <ADJ>* <Lperson> <ADJ>* (<P> <DET>* <NPP|NC|N|NER-Obj|Ploc> <CC>* <Lcom>*)* <ADJ>* <Lcom>? <NER-Obj|NPP>+}
		{<DET>* <ADJ>* <Lperson> <ADJ>* <NER-Obj|NPP>+}
	
	Porg:
		{<Lorg> <P>* <NER-Obj>}
		{<NER-Obj> <Lorg>}

	NER-Date:
		{<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
		{<DET>? <NER-Number> <NER-Month|NC> <NER-Number>}
		{<DET>? <NER-Number> <NER-Month>}

	NER-Money:
		{<NER-Number> <NC|N>* <Lmoney>}
"""

cp = RegexpParser(grammar)
tree = cp.parse(res)
print(tree)

dic = []
for subtree in tree.subtrees():
	if subtree.label() == "S":
		continue
	dic.append(tuple((subtree.label(), subtree.leaves())))
print(dic)

for i in range(len(dic)):
	if(dic[i][0] == "NER-Obj"):
