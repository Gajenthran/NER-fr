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
# & 


MONTH = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre|Décembre)$"
DAY = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)$"
PERSON = r"^(?:Data scientist|Statisticien|Analyste|Médecin|Échographiste|Mathématicien|Ingénieur|Pathologiste|Actuaire|Ergothérapeute|Directeur|Hygiéniste|Diététicien|Météorologue|Administrateur|Ophtalmologue|Thérapeute|Physicien|Chiropracteur|Technicien|Économiste|Responsable|Développeur|Pharmacien|Interprète|Traducteur|Rédacteur|Expert-Comptable|Agent|Juriste|Biologiste|Professeur|Podologue|Opticien|Libraire|Géologue|Orthodontiste|Écologiste|Manager|Artiste multimédia|Psychiatre|Dentiste|Vétérinaire|Psychologue|Programmeur|Conseiller d’orientation|Coiffeur|Historien|Assistant|Physiologiste|Consultant|Juge|Directeur|Principal|Zoologiste|Conservateur de musée|Dessinateur|Sociologue|Bijoutier|Physicien|Assureur|Comptable|Aide-enseignant|Dermatologue|Assistant|Dactylographe|Électricien|Assistant|Inspecteur|Chirurgien|Sténographe|Scientifique|Recruteur|Secrétaire médicale|Community Manager|Grossiste|Machiniste|Religieux|Monsieur|M|Mister|Mr|Messieurs|MM|Madame|Mme|Mesdames|Mmes|Mademoiselle|Mlle|Mesdemoiselles|Mlles|Veuve|Vve|Docteur|Dr|Docteurs|Drs|Maître|Maîtres|Professeur|Pr|Professeurs|Prs|Auditeur|Aud|Ingénieur Civil|Ir|Ingénieur Industriel|Ing|Duc|Duchesse|Marquis|Marquise|Comte|Cte|Comtesse|Ctesse|Vicomte|Vte|Vicomtesse|Vtesse|Baron|Bon|Baronne|Bonne|Seigneur|Sgr|Dame|Écuyer|Ec|Messire|Sir|Lady|Lord|Émir|Émira|Chérif|Chérifa|Cheikh|Cheykha|Bey|Calife|Hadjib|Nizam|Pervane|Sultan|Vizir|Râja|Rani|Malik|Shah|Padishah|Dom|Don|Père|P|Monsieur l'Abbé|Monsieur le Curé|Mère|M|Frère|Fr|Sœur|Sr|Révérend|Monseigneur|Mgr|Messeigneurs|Mgrs|Rabbin)$"


PONCT = r'(?:—|-|\.|!|\?|«|"|\')'
RULES = [
	# (r'(0[0-9]|1[0-9]|2[0-3]|[0-9])(?:\s*h\s*|\s*:\s*)[0-5][0-9]', "NER-Time"),
	# (r'(\d+)\s*(?:heures|heure|h|minute\w*|min|\w*seconde\w*|sec)', "NER-Time"),
	(PERSON, "Lperson"),

	(r"^[A-Z](?:[\.&]?[A-Z]){1,7}$", "NER-Acronym"),

	(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "NER-Mail"),

	(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', "NER-Date"),

	(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),

	(MONTH, "NER-Month"),
	# (r"((3[01]|[12][0-9]|[1-9])\s+)?(?:" + lst_exprs(trained_dic["NER-Month"]) + r")\s+\d+", "NER-Date"),

	(DAY, "NER-Day"),
	# (r"(?:" + lst_exprs(trained_dic["NER-Day"]) + r")", "NER-Day"),

	(r"^(?:-|\+)?\d*(?:\.|,)?\d+", "NER-Number"), # en lettre

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

ex = "Marco&Cie est mort."

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')
reg_words = r"Quelqu'un|Aujourd'hui|c'est-à-dire|\n\t\r|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´`]|\$[\d\.]+|quelqu'un|\w+[-\w+]+|aujourd'hui|prud'hom\w+|\w+|\S+"
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


grammar = r"""
	NER-Obj: 
		{<NER-Obj|N|NPP>+}

	NER-Date:
		{<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?}
		{<DET>? <NER-Number> <NER-Month|NC> <NER-Number>}
		{<DET>? <NER-Number> <NER-Month>}

"""

cp = RegexpParser(grammar)
print(cp.parse)


