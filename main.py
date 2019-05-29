from lexer import Lexer
from parser import Parser
from ner import NER
from tagger import Tagger
from util import Util
import argparse
import sys

"""
TODO:
	contenu dans le dossier tag pour la REN
	analyse sémantique à rajouter
	multi-thread?
	limitation du nombre de mot à tokenizer
"""

def usage(argv):
	"""
		REN = Reconnaissance d'Entités Nommées
		$ python3 main.py <test> <dest> [-d]
		De préférence le fichier <dest> devrait être un fichier xml pour 
		mieux voir les balises. Et l'option -d permettra de générer des
		modèles afin d'améliorer la REN mais augmente considérablement
		le temps d'exécution.
	"""
	print("Usage: " + str(argv[0]) + " <test.txt> <dest.xml> [-d]")
	sys.exit()

def main(argv):
	if len(argv) < 3:
		usage(argv)

	dic = False
	if len(argv) == 4:
		if argv[3] == "-d":
			dic = True

	ex = Util.read_file(argv[1])
	ex = Util.transform_text(ex)
	models = ["data/location.txt", "data/person.txt", "data/organisation.txt"]

	# Analyse lexicale
	lexer = Lexer(ex)
	lexer.lex()

	# Analyse syntaxique
	parser = Parser(lexer.get_tokenized_text())
	parser.parse()

	# Analyse sémantique + reconnaissance des EN
	ner = NER(ex, parser.get_parsed_text())
	if dic: ner.gen_models(models)
	ner.apply()

	# Balisage du texte
	tagger = Tagger(ner.get_ner(), ex);
	tagger.tag(argv[2])

if __name__ == '__main__':
	main(sys.argv)