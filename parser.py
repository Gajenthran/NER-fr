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

dico = {
	"PREP" : ["A", "Derrière", "Malgré", "Sauf", "Selon", "Avant", "Devant", "Sous", "Avec", 
			 "En", "Par", "Sur", "Entre", "Parmi", "Envers", "Pendant", "Vers", "Dans", "Pour", 
			 "De", "Près", "Depuis", "Sans"],

	"ADV"  : ['Bien', 'Vite', 'Mal', 'Beaucoup', 'Moins', 'Trop', 'Hier', 'Aujourd\'hui', 'Demain'],

	"PRON" : ["Je", "J'", "Tu", "Il", "Elle", "On", "Nous", "Vous", "Ils", "Elles", "Me", "M'", "Moi", "Te", 
			 "T'", "Toi", "Se", "Y", "Le", "Lui", "Soi", "Leur", "Eux", "Lui", "Qui", "Que", "Quoi", 
			 "Dont", "Où"],

	"CONJ" : ["Mais", "Ou", "Et", "Donc", "Or", "Ni", "Car", "Que", "Quand", "Comme", "Si", "Lorsque", 
			  "Quoique", "Puisque"],

	"DET" : ["Le", "La", "Les", "L'", "Un", "Une", "Des", "D'", "Du", "De", "Au", "Aux", "Ce", "Cet", 
			"Cette", "Ces", "Mon", "Son", "Ma", "Ta", "Sa", "Mes", "Ses", "Notre", "Votre", "Leur", 
			"Nos", "Vos", "leurs", "Aucun", "Aucune", "Aucuns", "Tel", "Telle", "Tels", "Telles", 
			"Tout", "Toute", "Tous", "Toutes", "Chaque"]
};

ponctuation = ['\\.', '\\!', '\\?', '\\:', '\\;', '\\,'];
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
"""
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

def read_file(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data

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
	# (r'(?<!' + ponctuation + r'(?!^)\b([A-Z]\w*(?:\s+[A-Z]\w*)*)', "NER-Obj"),
	(r"(?=[A-Z]\w*(?:\s+[A-Z]\w*)*)(?!" + gram_words + r")(?:[A-Z]\w*(?:\s+[A-Z]\w*)*)", "NER-Obj"),
	(r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*', "NER-lowerCamelCase"),
	(r'[a-z]+[A-Z0-9][a-z0-9]+[A-Za-z0-9]*', "NER-upperCamelCase")
]

def named_entities_match(text):
	ner_object = [];
	for rule in rules:
		for m in re.finditer(rule[0], text):
			ner_object.append(tuple((m.group(), rule[1])));


	"""
	compiled_regex = re.compile(rule[0]);
	matched = re.findall(compiled_regex, text);
	for match in matched:
		ner_object.append(tuple((match.group(), rule[1])));
	"""
	return ner_object;


def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def text_to_dict(text):
	dic = {}
	for line in text.splitlines():
		(key, value) = line.split(" - ");
		dic[key] = value;
	return dic;

def main(argv):
	if len(argv) != 3:
		usage(argv)
	
	trained_text = read_file(argv[1]);
	trained_dic = text_to_dict(trained_text);
	# print(trained_dic);

	tested_text = read_file(argv[2]);
	ner_object = named_entities_match(tested_text);
	print(ner_object);

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
