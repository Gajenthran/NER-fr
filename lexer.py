from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
from util import Util
import re

class Lexer:
	JAR = 'stanford-postagger/stanford-postagger-3.9.2.jar'
	MODEL = 'stanford-postagger/models/french.tagger'

	LEXEMES = r"Quelqu'un|Aujourd'hui|c'est-à-dire|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|[0-9]+\/[0-9]+\/[0-9]+|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´`]|\$[\d\.]+|quelqu'un|aujourd'hui|prud'hom\w+|\w+|\S+"

	MONTH_TAG = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre|Décembre|janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre|décembre)$"
	DAY_TAG = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)$"
	PERSON_TAG = r"^(?:roi|Roi|Reine|reine|reine|président|data scientist|statisticien|analyste|médecin|échographiste|mathématicien|ingénieur|pathologiste|actuaire|ergothérapeute|directeur|hygiéniste|diététicien|météorologue|administrateur|ophtalmologue|thérapeute|physicien|chiropracteur|technicien|économiste|responsable|développeur|pharmacien|interprète|traducteur|rédacteur|expert-comptable|agent|juriste|biologiste|professeur|podologue|opticien|libraire|géologue|orthodontiste|écologiste|manager|artiste multimédia|psychiatre|dentiste|vétérinaire|psychologue|programmeur|conseiller d’orientation|coiffeur|historien|assistant|physiologiste|consultant|juge|directeur|principal|zoologiste|conservateur de musée|dessinateur|sociologue|bijoutier|physicien|assureur|comptable|aide-enseignant|dermatologue|assistant|dactylographe|électricien|assistant|inspecteur|chirurgien|sténographe|scientifique|recruteur|secrétaire médicale|community manager|grossiste|machiniste|religieux|monsieur|m|mister|mr|messieurs|mm|madame|mme|mesdames|mmes|mademoiselle|mlle|mesdemoiselles|mlles|veuve|vve|docteur|dr|docteurs|drs|maître|maîtres|professeur|pr|professeurs|prs|auditeur|aud|ingénieur civil|ir|ingénieur industriel|ing|duc|duchesse|marquis|marquise|comte|cte|comtesse|ctesse|vicomte|vte|vicomtesse|vtesse|baron|bon|baronne|bonne|seigneur|sgr|dame|écuyer|ec|messire|sir|lady|lord|émir|émira|chérif|chérifa|cheikh|cheykha|bey|calife|hadjib|nizam|pervane|sultan|vizir|râja|rani|malik|shah|padishah|dom|don|père|monsieur l'abbé|monsieur le curé|mère|m|frère|fr|sœur|sr|révérend|monseigneur|mgr|messeigneurs|mgrs|rabbin)$"
	LOC_TAG = r"^(?:Aéroport|aéroport|Vallée|Université|université|sud|nord|ouest|Sud|Ouest|Nord|Rue|rue|Pays|Région|région|Cote|Côte|Place|Avenue|Passage|Pays|Allée|Boulevard|boulevard|Carrefour|carrefour|chemin|Chemin|Cité|cité|Cour|Esplanade|Impasse|Gallerie|gallerie|Pont|pont|Quai|quai|Route|route|Square|square|Terrasse|terrasse|Villa|ville)$"
	MONEY_TAG = r"^(?:€|\$|£|euros|euro|dollars|dollar|EUR|USD|yen|yens|dinar|dinars|GBP|francs|franc)$"
	NUMBER_TAG = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingts|vingt et un|trente|trente et un|quarante et un|quarante|cinquante et un|cinquante|soixante et un|soixante|soixante et onze|cent|cents|mille|milles|millions|million|milliard|milliards|billion|billions)"
	ORG_TAG = r"^(?:entreprise|\.inc|\.Inc|Agence|agence|groupe|Groupe|organisation|Organisation|Société|société)$"
	PUNC_TAG = r"^(?:…|»|«|—|–|-|’|ʼ|')$"
	RULES_TAG = [
		(r"^(?:|,|;|:)$", "Lcom"),
		(PERSON_TAG, "Lperson"),
		(LOC_TAG, "Lloc"),
		(ORG_TAG, "Lorg"),
		(MONEY_TAG, "Lmoney"),
		(MONTH_TAG, "Lmonth"),
		(DAY_TAG, "Lday"),
		(r"^" + NUMBER_TAG + r"-" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^[A-Z](?:\.[A-Z]){1,7}$", "Lacronym"),
		(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "Lmail"),
		(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', "Ldate"),
		(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "Lurl"),
		(r"^(?:-|\+)?\d*(?:\.|,)?\d+$", "Lnumber"), # en lettre
		(r"^[A-Z]\w*-\w\w*$", "Lobj"),
		(r"^[a-z_]+[A-Z0-9_][a-z0-9_]*$", "Lobj"),
		(r'^[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*$', "Lobj"),
		(r"^[A-Z]\w*$", "Lobj"),
		(PUNC_TAG, "PUNC"),
	]

	def __init__(self, text):
		self.text = text
		self.tagged_tokens = []

	def lex(self):
		self.text = Util.transform_text(self.text)

		pos_tagger = StanfordPOSTagger(Lexer.MODEL, Lexer.JAR, encoding='utf8')
		tokenizer = RegexpTokenizer(Lexer.LEXEMES)
		self.tagged_tokens = pos_tagger.tag(tokenizer.tokenize(self.text))
		
		for i in range(0, len(self.tagged_tokens)):
			for rt in Lexer.RULES_TAG:
				for m in re.finditer(rt[0], self.tagged_tokens[i][0]):
					if (i == 0 and rt[1] == "Lobj") or (i > 0 and self.tagged_tokens[i-1][1] == "PUNC" and rt[1] == "Lobj"):
						continue
					if self.tagged_tokens[i][1].startswith("L"):
						continue
					self.tagged_tokens[i] = tuple((m.group(), rt[1]))
		print(self.tagged_tokens)

	def get_tokens(self):
		return self.tagged_tokens