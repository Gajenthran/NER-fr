from idl_lexer import Lexer
from idl_parser import Parser
from idl_ner import NER
from idl_tagger import Tagger
from util import Util

ex = "Laurent Azerty est mort."
ex = Util.read_file("Fusion_Animal_Hum_Corpus_v3_FR_utf8.txt")

ex = Util.transform_text(ex)
lexer = Lexer(ex)
lexer.lex()
parser = Parser(lexer.get_tokens())
parser.parse()

ner = NER(ex, parser.get_tagged_tokens())
ner.gen_models(["data/location.txt", "data/person.txt"])
ner.apply()
tagger = Tagger(ner.get_ner(), ex);
tagger.tag("fifi.txt")
exit()