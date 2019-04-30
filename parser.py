import nltk, nltk.data, nltk.tag
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.chunk import RegexpParser
import codecs
import os
import sys
import re

# ponctuation
# nature en francais
# stopwords
# probabilité words
# det != pp
# preposition
# enlever point virgule en Python


def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

def text_to_dict(text):
	dic = {}
	for line in text.splitlines():
		(key, value) = line.split(" : ");
		value = value.split(", ");
		dic[key] = value;
	return dic;

def dict_to_text(dic):
	text = "";
	for key, value in dic.items():
		text += key + " : " + ', '.join(value) + "\n";
	return text;


trained_dic = -1;
trained_text = read_file("ner-object.txt");
trained_dic = text_to_dict(trained_text);

dico = {
	'PREP': ['À', 'A', 'Après', 'Attendu', 'Au-dedans', 'Au-dehors', 'Au-delà', 'De', "D'", "D’", 'Au-dessous', 'Au-dessus', 
	'Auprès', 'Autour', 'Auxenviron', 'Avant', 'Avec', 'Avecque', 'Centi-', 'Chez', 'Concernant', 'Contre', 
	'Dans', 'De', 'Depuis', 'Derrière', 'Des', 'Devant', 'Devers', 'Dixit', 'Durant', 'Emmi', 'En', 
	'Entre', 'Envers', 'Excepté', 'Hormis', 'Hors', 'Jusque', 'Jusqu', 'Malgré', 'Moyennant', 'Nonobstant', 
	'Outre', 'Par', 'Parmi', 'Passé', 'Pendant', 'Pico-', 'Pour', 'Près', 'Proto-', 'Quant à', 'Revoici', 
	'Revoilà', 'Rez', 'Sans', 'Sauf', 'Selon', 'Sous', 'Sub', 'Suivant', 'Sur', 'Vers', 'Versus', 'Via', 
	'Vis-à-vis', 'Voici', 'Voilàa', 'Derrière', 'Malgré', 'Sauf', 'Selon', 'Avant', 'Devant', 'Sous', 'Avec', 
	'En', 'Par', 'Sur', 'Entre', 'Parmi', 'Envers', 'Pendant', 'Vers', 'Dans', 'Pour', 'De', 'Près', 'Depuis', 'Sans'], 

	'ADV': ['Admirablement', 'Ainsi', 'Aussi', 'Bien', 'Comme', 'Comment', 'Debout', 'Doucement', 'Également', 
	'Ensemble', 'Exprès', 'Franco', 'Gratis', 'Impromptu', 'Incognito', 'Lentement', 'Mal', 'Mieux', 'Pis', 
	'Plutôt', 'Presque', 'Recta', 'Vite', 'Volontiers', 'Ainsi', 'À peine', 'À peu près', 'Absolument', 'Demi', 
	'Assez', 'Aussi', 'Autant', 'Autrement', 'Approximativement', 'Beaucoup', 'Carrément', 'Combien', 'Comme', 
	'Complètement', 'Davantage', 'À demi', 'Diablement', 'Divinement', 'Drôlement', 'Encore', 'Entièrement', 
	'Environ', 'Extrêmement', 'Fort', 'Grandement', 'Guère', 'Infiniment', 'Insuffisamment', 'Joliment', 'Même', 
	'Moins', 'Pas mal', 'Passablement', 'Peu', 'Plus', 'Plutôt', 'Presque', 'Prou', 'Quasi', 'Quasiment', 'Quelque', 
	'Rudement', 'Si', 'Suffisamment', 'Tant', 'Tellement', 'Terriblement', 'Totalement', 'Tout', 'Tout à fait', 
	'Très', 'Trop', 'Trop peu', 'Tout à fait', 'Un peu', 'Alors', 'Après', 'Après-demain', "Aujourd'hui", 
	'Auparavant', 'Aussitôt', 'Autrefois', 'Avant', 'Avant-hier', 'Bientôt', 'Cependant', "D'abord", 'Déjà', 
	'Demain', 'Depuis', 'Derechef', 'Désormais', 'Dorénavant', 'Encore', 'Enfin', 'Ensuite', 'Entre-temps', 
	'Hier', 'Jadis', 'Jamais', 'Longtemps', 'Lors', 'Maintenant', 'Naguère', 'Parfois', 'Plus', 'Premièrement', 
	'Puis', 'Quand', 'Quelquefois', 'Sitôt', 'Soudain', 'Souvent', 'Subito', 'Tantôt', 'Tard', 'Tôt', 'Toujours', 
	'Ailleurs', 'Alentour', 'Alentours', 'Arrière', 'Au-delà', 'Au-dessous', 'Au-dessus', 'Au-devant', 'Autour', 
	'Avant', 'Ça', 'Céans', 'Ci', 'Contre', 'Deçà', 'Dedans', 'Dehors', 'Derrière', 'Dessous', 'Dessus', 'Devant', 
	'Ici', 'Là', 'Là-haut', 'Loin', 'Où', 'Outre', 'Partout', 'Près', 'Proche', 'Sus', 'Y', 'Apparemment', 
	'Assurément', 'Aussi', 'Bien', 'Bon', 'Certainement', 'Certes', 'En vérité', 'Oui', 'Peut-être', 'Précisément', 
	'Probablement', 'Sans doute', 'Si', "S’", "S'", 'Soit', 'Tout à fait', 'Toutefois', 'Volontiers', 'Vraiment', 
	'Vraisemblablement', 'Aucunement', 'Guère', 'Jamais', 'Ne', "N’", "N'", 'Non', 'Nullement', 'Pas', 'Plus', 'Rien'], 

	'PRON': ['Je', "J'", "J’", "me", "M'", "M’", 'Moi', 'Tu', 'Te', "T'", "T’", 'Toi', 'Nous', 'Vous', 'Il', 'Elle', 'Ils', 'Elles', 
	'Se', 'En', 'Y', 'Le', 'La', "L'", "L’", 'Les', 'Lui', 'Soi', 'Leur', 'Eux', 'Lui', 'Leur', 'Celui', 'Celui-ci', 'Celui-là', 
	'Celle', 'Celle-ci', 'Celle-là', "C'", "C’", "Ceux", 'Ceux-ci', 'Ceux-là', 'Celles', 'Celles-ci', 'Celles-là', 'Ce', 'Ceci', 'Cela', 
	'Ça', 'Le mien', 'Le tien', 'Le sien', 'La mienne', 'La tienne', 'La sienne', 'Les miens', 'Les tiens', 
	'Les siens', 'Les miennes', 'Les tiennes', 'Les siennes', 'Le nôtre', 'Le vôtre', 'Le leur', 'La nôtre', 'La vôtre', 
	'La leur', 'Les nôtres', 'Les vôtres', 'Les leurs', 'Qui', 'Que', 'Quoi', 'Dont', 'Où', 'Lequel', 'Auquel', 
	'Duquel', 'Laquelle', 'À laquelle', 'De laquelle', 'Lesquels', 'Auxquels', 'Desquels', 'Lesquelles', 'Auxquelles', 
	'Desquelles', 'Qui', 'Que', 'Quoi', "Qu'est-ce", 'Lequel', 'Auquel', 'Duquel', 'Laquelle', 'À laquelle', 
	'De laquelle', 'Lesquels', 'Auxquels', 'Desquels', 'Lesquelles', 'Auxquelles', 'Desquelles', 'On', 'Tout', 'Un', 
	'Une', "L'un", "L'une", 'Les uns', 'Les unes', 'Un autre', 'Une autre', "D'autres", "L'autre", 'Les autres', 
	'Aucun', 'Aucune', 'Aucuns', 'Aucunes', 'Certains', 'Certaine', 'Certains', 'Certaines', 'Tel', 'Telle', 'Tels', 
	'Telles', 'Tout', 'Toute', 'Tous', 'Toutes', 'Le même', 'La même', 'Les mêmes', 'Nul', 'Nulle', 'Nuls', 'Nulles', 
	"Quelqu'un", "Quelqu'une", 'Quelques uns', 'Quelques unes', 'Quelques', 'Quelque', 'Personne', 'Autrui', 'Quiconque', "D'aucuns"], 

	'CONJ': ['Mais', 'Ou', 'Et', 'Donc', 'Or', 'Ni', 'Car', 'Que', 'Quand', 'Comme', 'Si', 'Lorsque', 'Quoique', 
	'Puisque'], 

	'DET': ['Le', 'La', 'Les', "L'", 'Un', 'Une', 'Des', "D'", 'Du', 'De', 'Au', 'Aux', 'Ce', 'Cet', 'Cette', 'Ces', 
	'Mon', 'Son', 'Ma', 'Ta', 'Sa', 'Mes', 'Ses', 'Notre', 'Votre', 'Leur', 'Nos', 'Vos', 'Leurs', 'Aucun', 'Aucune', 
	'Aucuns', 'Tel', 'Telle', 'Tels', 'Telles', 'Tout', 'Toute', 'Tous', 'Toutes', 'Chaque']
};

ex = 'On est le 12/10/2019';

def mw(words):
	combineWord = "";
	for i in range(0, len(words)):
		combineWord += words[i] + "|";

	combineWord = combineWord[:-1];
	return "\\b(?:" + combineWord + ")\\b";

def mp(words):
	combineWord = "";
	for i in range(0, len(words)):
		combineWord += words[i] + "|";

	combineWord = combineWord[:-1];
	return "(?:" + combineWord + ")";
r"""
rules = [
	mw(prep) + "\\s+" + mw(det),
	mw(adv) + "\\s+" + mw(det),
	mp(ponctuation) + "\\s*" + mw(det), # (?:\!|\,|\.|\;|\?|\:|\.\.\.)\s*(?:le|la|un)\b
	mw(pp) + "\\s+" + mw(det)
];
"""
forbidden_rules = [3];
"""
def matchPattern(words1, words2):
	global rules;
	for i in range(0, len(rules)):
		reg = re.compile(rules[i], re.IGNORECASE);
		print(re.findall(reg, ex));
"""
def matchSimple():
	reg = re.compile(r"\b(?:le|la|un)\b", re.IGNORECASE);
	print(re.findall(reg, ex));

def transform(words):
	for i in range(0, len(words)):
		words[i] = words[i].lower();
	return words;


def parse_det(txt):
	words = transform(nltk.word_tokenize(txt));
	for w in words:
		if w in det:
			get_det.append(w);
	return words;

def freq_word(words):
	freq = FreqDist();
	for w in words:
		freq[w.lower] += 1;
	print(freq);

def usage(argv):
	print("Usage: " + str(argv[0]) + " <trained_text> <source>")
	sys.exit()

def lst_exprs(expressions):
	reg = r'';
	for expr in expressions:
		reg += r'\b(' + expr + r')\b|';
	reg = reg[:-1];
	return reg;

ponctuation = r'(?:—|-|\.|!|\?|«|"|\')';
gram_words = lst_exprs(dico["DET"])  + r'|' + \
			 lst_exprs(dico["CONJ"]) + r'|' + \
			 lst_exprs(dico["ADV"])  + r'|' + \
			 lst_exprs(dico["PRON"]) + r'|' + \
			 lst_exprs(dico["PREP"]);

rules = [
	(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", "NER-Mail"),
	(r'(0[0-9]|1[0-9]|2[0-3]|[0-9])(?:\s*h\s*|\s*:\s*)[0-5][0-9]', "NER-Time"),
	(r'(\d+)\s*(?:heures|heure|h|minute\w*|min|\w*seconde\w*|sec)', "NER-Time"),
	(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?', "NER-URL"),
	(r'([0-2][0-9]|(3)[0-1])(?:\/|-)(((0)[0-9])|((1)[0-2]))(?:\/|-)\d{4}', "NER-Date"),
	(r"(?:-|\+)?\d*(?:\.|,)?\d+", "NER-Number"), # en lettre
	(r"(?<!" + ponctuation + r"\s)(?!^)\b([A-Z]\w*(?:(?:\s+|-|\.)[A-Z]\w*)*)", "NER-Obj"),
	# (r"(?=[A-Z]\w*(?:\s+[A-Z]\w*)*)(?!" + gram_words + r")(?:[A-Z]\w*(?:\s+[A-Z]\w*)*)", "NER-Obj"),
	(r'[a-z]+[A-Z0-9]\w*', "NER-lowerCamelCase"),
	(r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*', "NER-upperCamelCase"),
	(r"(?:" + lst_exprs(trained_dic["NER-Day"]) + r")", "NER-Day"),
	(r"(?:" + lst_exprs(trained_dic["NER-Person"]) + r")", "NER-Person"),
	(r"(?:" + lst_exprs(trained_dic["NER-Sugg"]) + r")", "NER-Sugg"),
]

def named_entities_match(text):
	ner_object = [];
	for rule in rules:
		for m in re.finditer(rule[0], text):
			ner_object.append(tuple((m.group(), rule[1], m.start(), m.end())));
			trained_dic["NER-Sugg"].append(m.group());

	"""
	compiled_regex = re.compile(rule[0]);
	matched = re.findall(compiled_regex, text);
	for match in matched:
		ner_object.append(tuple((match.group(), rule[1])));
	"""
	return ner_object;



def clean_trained_dict(dic):
	words = list(set(dic["NER-Sugg"]));
	dic["NER-Sugg"] = words;
	return dic;


def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def ne_rm_duplicate(lst):
	filtered_lst = []
	rm_lst = [];
	# print(lst);
	for i in range(0, len(lst)):
		start = lst[i][2];
		end = lst[i][3];
		founded = i;
		for j in range(0, len(lst)):
			if lst[j][2] == start and lst[j][3] >= end:
				rm_lst.append(founded);
				founded = j;
				end = lst[j][3];
	# print(rm_lst)
	return filtered_lst

def main(argv):
	if len(argv) != 3:
		usage(argv)
	
	global trained_dic;
	# trained_text = read_file(argv[1]);
	# trained_dic = text_to_dict(trained_text);
	# print(trained_dic);

	tested_text = read_file(argv[2]);
	ner_object = named_entities_match(tested_text);
	print(ner_object);

	trained_dic = clean_trained_dict(trained_dic);
	write_file("ner-object.txt", dict_to_text(trained_dic));
	r"""
	txt = ex.split();
	pattern = "les";
	add = "|";
	reg_words = r"(?<!\.\s)(?!^)\b([A-Z]\w*(?:\s+[A-Z]\w*)*)|les";
	tok = RegexpTokenizer(reg_words);
	print(tok.tokenize(ex));
	"""
	# print(re.findall(ex));
	# print(tok.tokenize(txt));
	# t.concordance("je", width=50, lines=10)
	# matchPattern(adv, det);

if __name__ == '__main__':
	main(sys.argv)
