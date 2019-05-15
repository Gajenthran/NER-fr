class Util:
	def __init__(self):
		print("toto")

	@staticmethod
	def read_file(filename):
		with open(filename, 'r') as file:
			data = file.read()
		return data

	@staticmethod
	def text_to_dic(text):
		dic = {}
		for line in text.splitlines():
			(key, value) = line.split(" : ")
			value = value.split("\n")
			dic[key] = value
		return dic

	@staticmethod
	def dic_to_text(dic):
		text = ""
		for key, value in dic.items():
			text += key + "\n" + '\n'.join(value)
		return text

	@staticmethod
	def write_file(filename, data):
		with open(filename, 'w') as file:
			file.write(data)


	@staticmethod
	def to_rgx(expressions):
	    reg = r'';
	    for expr in expressions:
	        reg += r'\b(' + expr + r')\b|';
	    reg = reg[:-1];
	    return reg;

	@staticmethod
	def prioritize_obj(lst):
		i = 0
		length = len(lst)
		while i < length:
			j = i + 1
			if not(j < length): break
			if lst[j][1] != "NER-Obj":
				while j < length:
					if lst[j][2] == lst[i][2] and lst[j][3] == lst[i][3]:
						lst[i] = 0
					j += 1
			i += 1

		lst = Util.rm_duplicate(lst)
		return lst

	@staticmethod
	def rm_duplicate(lst):
		i = 0
		n = 0
		length = len(lst)
		while i < length:
			if lst[i] == n:
				lst.remove(lst[i])
				length = length -1  
				continue
			i = i+1

		return lst

	def sort_ner(lst):
		for element in lst:
			if element[1] == "NER-Obj":
				lst.remove(element)
				lst.insert(0, element)
		return lst

	@staticmethod
	def transform_text(text):
		text = text.replace("(" , " ( ")
		text = text.replace(")" , " ) ")
		text = text.replace("{" , " { ")
		text = text.replace("}" , " } ")
		text = text.replace("\"", " \" ")
		text = text.replace("'", "' ")
		text = text.replace(", ", " , ")
		return text

	@staticmethod
	def detransform_text(text):
		text = text.replace("' "   , "'")
		text = text.replace(" , "  , ", ")
		text = text.replace(" ( " , "(")
		text = text.replace(" ) " , ")")
		text = text.replace(" { " , "{")
		text = text.replace(" } " , "}")
		text = text.replace(" \" ", "\"")
		return text	
