class Util:
	def __init__(self):
		print("toto")

	@staticmethod
	def read_file(filename):
		with open(filename, 'r') as file:
			data = file.read()
		return data

	@staticmethod
	def text_to_dict(text):
		dic = {}
		for line in text.splitlines():
			(key, value) = line.split(" : ")
			value = value.split("\n")
			dic[key] = value
		return dic

	@staticmethod
	def dict_to_text(dic):
		text = ""
		for key, value in dic.items():
			text += key + " : " + ', '.join(value) + "\n"
		return text

	@staticmethod
	def write_file(filename, data):
		with open(filename, 'w') as file:
			file.write(data)


	@staticmethod
	def to_regex(expressions):
	    reg = r'';
	    for expr in expressions:
	        reg += r'\b(' + expr + r')\b|';
	    reg = reg[:-1];
	    return reg;
