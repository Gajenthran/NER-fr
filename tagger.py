from util import Util

class Tagger:
	def __init__(self, named_entities, text):
		self.tagged_text = text
		# entity(word, object, start, end)
		self.named_entities = named_entities
		self.notag = True

	def insert_tag(self, source, start, ne):

		# balise ouvrante
		position = start + ne[2]
		tag = '<NER cat="' + ne[1] + '">'
		source = source[:position] + tag + source[position:]
		position = ne[3] + start + len(tag)

		# balise fermante
		tago = tag
		tag = '</NER>'
		source = source[:position] + tag + source[position:]
		position = len(tago) + len(tag) 

		return source, position

	def subtag(self, source, position):
		"""
			Vérification des sous-balises. Pour cela, on vérifie simplement si une balise est 
			contenu dans une balise ou pas. On regarde la dernière balise à partir de la position
			actuelle : si il s'agit d'une balise ouvrante alors il s'agit d'une sous-balise sinon
			il ne s'agit pas d'une s'agit balise.

			:param source: le fichier source
			:param position: position à laquelle nous devons ajouter la balise ouvrante
		"""
		if self.notag == True:
			self.notag = False
			return False

		i = position
		while i > 0 and (source[i] != '<' or (source[i] == '<' and source[i + 1] == ' ')):
			i -= 1
		if((source[i] == '<' and source[i + 1] == '/')):
			return False
		return True


	def tag(self, dest_file):
		"""
			Transformer le fichier texte donnée en entrée en fichier .xml en balisant les mots 
			du dictionnaire

			:param txt: fichier texte       
		"""
		beg = 0
		end = 0
		for ne in self.named_entities:
			pos = ne[2] + beg
			if end > ne[2]: continue
			if not(self.subtag(self.tagged_text, pos)):
				self.tagged_text, end = self.insert_tag(self.tagged_text, beg, ne)
				beg += end
				end = ne[3]

		self.tagged_text = Util.detransform_text(self.tagged_text)
		Util.write_file(dest_file, self.tagged_text)