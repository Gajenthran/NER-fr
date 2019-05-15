from nltk.tokenize import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
from util import Util
import re

class Lexer:
	JAR = 'stanford-postagger/stanford-postagger-3.9.2.jar'
	MODEL = 'stanford-postagger/models/french.tagger'

	LEXEMES = r"Quelqu'un|Aujourd'hui|c'est-à-dire|[0-9]+\/[0-9]+\/[0-9]+|\w+[-\w+]+|\w+[\/\w+]+|\b[A-Z](?:[\.&]?[A-Z]){1,7}\b|(?:-|\+)?\d*(?:\.|,)?\d+|\d+|\w['´`]|\$[\d\.]+|quelqu'un|aujourd'hui|prud'hom\w+|\w+|\S+"

	MONTH_TAG = r"^(?:Janvier|Février|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre|Décembre|janvier|février|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre|décembre)$"
	DAY_TAG = r"^(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)$"
	PERSON_TAG = r"^(?:Président|roi|Roi|Reine|reine|président|Data scientist|Statisticien|Analyste|Médecin|Échographiste|Mathématicien|Ingénieur|Pathologiste|Actuaire|Ergothérapeute|Directeur|Hygiéniste|Diététicien|Météorologue|Administrateur|Ophtalmologue|Thérapeute|Physicien|Chiropracteur|Technicien|Économiste|Responsable|Développeur|Pharmacien|Interprète|Traducteur|Rédacteur|Expert-Comptable|Agent|Juriste|Biologiste|Professeur|Podologue|Opticien|Libraire|Géologue|Orthodontiste|Écologiste|Manager|Artiste multimédia|Psychiatre|Dentiste|Vétérinaire|Psychologue|Programmeur|Conseiller d’orientation|Coiffeur|Historien|Assistant|Physiologiste|Consultant|Juge|Directeur|Principal|Zoologiste|Conservateur de musée|Dessinateur|Sociologue|Bijoutier|Physicien|Assureur|Comptable|Aide-enseignant|Dermatologue|Assistant|Dactylographe|Électricien|Assistant|Inspecteur|Chirurgien|Sténographe|Scientifique|Recruteur|Secrétaire médicale|Community Manager|Grossiste|Machiniste|Religieux|Monsieur|M|Mister|Mr|Messieurs|MM|Madame|Mme|Mesdames|Mmes|Mademoiselle|Mlle|Mesdemoiselles|Mlles|Veuve|Vve|Docteur|Dr|Docteurs|Drs|Maître|Maîtres|Professeur|Pr|Professeurs|Prs|Auditeur|Aud|Ingénieur Civil|Ir|Ingénieur Industriel|Ing|Duc|Duchesse|Marquis|Marquise|Comte|Cte|Comtesse|Ctesse|Vicomte|Vte|Vicomtesse|Vtesse|Baron|Bon|Baronne|Bonne|Seigneur|Sgr|Dame|Écuyer|Ec|Messire|Sir|Lady|Lord|Émir|Émira|Chérif|Chérifa|Cheikh|Cheykha|Bey|Calife|Hadjib|Nizam|Pervane|Sultan|Vizir|Râja|Rani|Malik|Shah|Padishah|Dom|Don|Père|P|Monsieur l'Abbé|Monsieur le Curé|Mère|M|Frère|Fr|Sœur|Sr|Révérend|Monseigneur|Mgr|Messeigneurs|Mgrs|Rabbin)$"
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
		(MONTH_TAG, "NER-Month"),
		(DAY_TAG, "NER-Day"),
		(r"^" + NUMBER_TAG + r"-" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^" + NUMBER_TAG + r"$", "Lnumber"), # en lettre
		(r"^[A-Z](?:\.[A-Z]){1,7}$", "NER-Acronym"),
		(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "NER-Mail"),
		(r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', "NER-Date"),
		(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),
		(r"^(?:-|\+)?\d*(?:\.|,)?\d+$", "Lnumber"), # en lettre
		(r"^[A-Z]\w*-\w\w*$", "NER-Obj"),
		(r"^[a-z_]+[A-Z0-9_][a-z0-9_]*$", "NER-Obj"),
		(r'^[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*$', "NER-Obj"),
		(r"^[A-Z]\w*$", "NER-Obj"),
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
					if (i == 0 and rt[1] == "NER-Obj") or (i > 0 and self.tagged_tokens[i-1][1] == "PUNC" and rt[1] == "NER-Obj"):
						continue
					if self.tagged_tokens[i][1].startswith("NER-") or self.tagged_tokens[i][1].startswith("L"):
						continue
					self.tagged_tokens[i] = tuple((m.group(), rt[1]))



	def get_tokens(self):
		return self.tagged_tokens