import sys
from util import Util
from ner import NER
from tagger import Tagger

# ponctuation
# nature en francais
# stopwords
# probabilité words
# det != pp
# preposition
# enlever point virgule en Python
# accent + e dans le o
# temps : en depuis, avant, environ après, 1930, durant, dans, an, 
# lieu  : chez, à, vers, 
# pers  : selon, 

dico = {
    'PREP': ['À', 'A', 'Après', 'Attendu', 'Au-dedans', 'Au-dehors', 'Au-delà', 'De', "D'", "D’", 'Au-dessous', 'Au-dessus', 
    'Auprès', 'Autour', 'Auxenviron', 'Avant', 'Avec', 'Avecque', 'Centi-', 'Chez', 'Concernant', 'Contre', 
    'Dans', 'De', 'Depuis', 'Derrière', 'Des', 'Devant', 'Devers', 'Dixit', 'Durant', 'Emmi', 'En', 
    'Entre', 'Envers', 'Excepté', 'Hormis', 'Hors', 'Jusque', 'Jusqu', 'Malgré', 'Moyennant', 'Nonobstant', 
    'Outre', 'Par', 'Parmi', 'Passé', 'Pendant', 'Pico-', 'Pour', 'Près', 'Proto-', 'Quant à', 'Revoici', 
    'Revoilà', 'Rez', 'Sans', 'Sauf', 'Selon', 'Sous', 'Sub', 'Suivant', 'Sur', 'Vers', 'Versus', 'Via', 
    'Vis-à-vis', 'Voici', 'Voilà', 'Voila', 'Derrière', 'Malgré', 'Sauf', 'Selon', 'Avant', 'Devant', 'Sous', 'Avec', 
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

"""
def clean_trained_dict(dic):
    words = list(set(dic["NER-Sugg"]));
    dic["NER-Sugg"] = words;
    return dic;
"""


def usage(argv):
    print("Usage: " + str(argv[0]) + " <model_txt> <test_txt> <tagged_txt>")
    sys.exit()

def main(argv):
    if len(argv) != 4:
        usage(argv)

    test_text = Util.read_file(argv[2])

    ner = NER(test_text)
    ner.create(["data/person.txt", "data/location.txt", "data/movie.txt"])
    ner.match()
    ner.rm_duplicate()

    tagger = Tagger(ner.get_words(), test_text);
    tagger.tag(argv[3])



    """
    train = Train()
    train.trainModels((["data/person.txt", "data/location.txt", "data/movie.txt"]))
    trained_dic = trainModels(["data/person.txt", "data/location.txt", "data/movie.txt"])
    # print(trained_dic);

    tested_text = read_file(argv[2]);
    ner_object = named_entities_match(tested_text);
    ner_object = ne_rm_duplicate(ner_object);
    """
    
    # trained_dic = clean_trained_dict(trained_dic);
    # write_file("ner-object.txt", dict_to_text(trained_dic));
    # print(ner_object);
    # print(ner_object)
    # print(txt_to_xml(tested_text, ner_object));

    # print(re.findall(ex));
    # print(tok.tokenize(txt));
    # t.concordance("je", width=50, lines=10)
    # matchPattern(adv, det);

if __name__ == '__main__':
    main(sys.argv)
