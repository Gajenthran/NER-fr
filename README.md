# Reconnaissance d'Entités Nommées (NER)

La reconnaissance d'entités nommées est une sous-tâche de l'activité d'extraction d'information dans des corpus documentaires. Elle consiste à rechercher des objets textuels (c'est-à-dire un mot, ou un groupe de mots) catégorisables dans des classes telles que noms de personnes, noms d'organisations ou d'entreprises, noms de lieux, quantités, distances, valeurs, dates, etc (source Wikipédia).


# Usage

```
python3 main.py <test.txt> <dest.xml> [-d]
```
Il est plutôt recommendé que le fichier ```dest``` soit un fichier ```xml``` pour le balisage. 
L'option ```[-d]``` permet de faire appel aux modèles afin d'obtenir une reconnaissance plus accrue des entités nommées mais augmente considérablement le temps de d'exécution.
Par exemple,
```
python3 main.py test.txt fifi.xml
```

# Etapes menant à la reconnaissance

Une approche naïve aurait été de reconnaître tous les mots en majuscules cependant cette méthode est assez limitée dans le sens où on sera très rapidement confronté à de nombreuses ambiguïtés comme celle des mots en début de phrase. Pour cela, nous allons essayé de jouer sur la syntaxe et sur un modèle donné afin de renforcer la REN.

## Analyse lexicale

Avant de vérfier la syntaxe et le contexte du texte, nous allons tout d'abord formater le texte et le tokénizer.
La modification du texte passe par la modification de certains caractères spéciaux notamment les apostrophes qui auront du mal à être reconnu par notre analyse lexicale. 
Une fois le texte modifié, nous pouvons procéder à une analyse lexicale qui consiste à couper tous les "mots" du texte en lexèmes, où on pourra donner à chacun un type nommé "tag". De plus nous retiendrons la position du début et de fin de chaque lexème afin de pouvoir faciliter le balisage.
Pour cela on s'aidera de ```StanfordPOSTagger``` pour tagger une grande partie des mots (notamment pour les classes grammaticales) et on définira certains mots selon notre dictionnaire de tag pour aider l'analyse syntaxique.

## Analyse syntaxique
Dans l'analyse syntaxique, on va pouvoir définir notre grammaire pour identifier toutes EN, pour l'instant seulement le contexte gauche. Une preuve externe va permettre justement dans un premier temps, d'identifier une possible entité nommée et enfin si ce n'est pas le cas on effectuera une preuve interne.
Par exemple pour une date peut être défini de la manière suivante: 
- ```<DET>? <NER-Day|NC> <NER-Number> <NER-Month> <NER-Number>?``` un ```NER-Day``` qui correspond à un jour de l'année suivi d'un ```NER-Number``` qui est un nombre, suivi lui-même d'un mois (```NER-Month```) et possiblement d'un autre nombre (qui correspondra à l'année). Mais il y a également d'autres manières de le faire et c'est dans cette partie là que nous allons tous les définir.

- Preuve externe = mot contenu dans la NE permettant de donner une information sur le type de la EN. Par exemple, la Banque Populaire, nous savons que Banque Populaire est une EN et le mot "Banque" permet de montrer que c'est une NE de type "organisation". 
- Preuve interne = mot en dehors de la NE permettant de donner une information sur le type de la EN, on parle alors de contexte gauche et contexte droit. Par exemple pour le président de la France, Macron, Macron est NE et le groupe de mot président de la France permet de dire qu'il s'agit d'une personne. 
- Définir la preuve externe avant la preuve interne est important car la preuve externe dépend du contexte. Par exemple, si nous avons la reine de Wiwi, Paris Hilton, le mot "Paris" peut nous faire croire qu'il s'agit d'un lieu mais ici il s'agit d'une personne et c'est le groupe de mot "reine de Wiwi" qui nous indique cela.


## Analyse sémantique + NE
L'analyse sémantique va nous permettre de vérifier le sens des NE que nous avons identifié prédémment. Notamment la date, en vérifiant si les nombres sont bien des jours de l'année (compris entre 0 et 31) par exemple. Une fois les vérifications terminées, nous pouvons utiliser les modèles afin d'améliorer notre reconnaissance.

## Tagger
Une fois les analyses terminées, nous allons pouvoir tagger notre texte de la manière suivante: ```<NER cat=[type]></NER>``` où ```NER``` correspond à Named Entities Recognition.
