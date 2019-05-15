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

	def transform_text(text):
		text = text.replace("(" , " ( ")
		text = text.replace(")" , " ) ")
		text = text.replace("{" , " { ")
		text = text.replace("}" , " } ")
		text = text.replace("\"", " \" ")
		text = text.replace("'", "' ")
		text = text.replace(", ", " , ")
		return text

	def detransform_text(text):
		text = text.replace("' "   , "'")
		text = text.replace(" , "  , ", ")
		text = text.replace(" ( " , "(")
		text = text.replace(" ) " , ")")
		text = text.replace(" { " , "{")
		text = text.replace(" } " , "}")
		text = text.replace(" \" ", "\"")
		return text	
