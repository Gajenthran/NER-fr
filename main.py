from lexer import Lexer
from parser import Parser
from ner import NER
from tagger import Tagger
from util import Util
import argparse
import sys

# preuve interne
# organisations
# commentaires
# enlever majuscules dans tag

def usage(argv):
    print("Usage: " + str(argv[0]) + " <test_txt> <tagged_txt> [-d]")
    sys.exit()

def main(argv):
	if len(argv) < 3:
		usage(argv)

	dic = True
	if len(argv) == 4:
		if argv[3] == "-d":
			dic = False

	# ex = "Le président de la République, François Mitterand"
	ex = Util.read_file(argv[1])
	ex = Util.transform_text(ex)
	models = ["data/location.txt", "data/person.txt", "data/organisation.txt"]

	# Analyse lexicale
	lexer = Lexer(ex)
	lexer.lex()

	# Analyse syntaxique
	parser = Parser(lexer.get_tokenized_text())
	parser.parse()

	# Analyse sémantique + NE
	ner = NER(ex, parser.get_parsed_text())
	if dic: ner.gen_models(models)
	ner.apply()

	# Balisage du texte
	tagger = Tagger(ner.get_ner(), ex);
	tagger.tag(argv[2])

if __name__ == '__main__':
	main(sys.argv)