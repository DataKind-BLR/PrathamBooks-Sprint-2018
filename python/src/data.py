import getopt, sys, csv
from bs4 import BeautifulSoup, Comment

# Argument phraser
opts, args = getopt.getopt(sys.argv[1:], 'i:o:')

file_in = None
file_out = None
for o, a in opts:
	if o == '-i':
		file_in = a
	elif o == '-o':
		file_out = a

# Data extraction
data = []
with open(file_in) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		data.append(row)

# Clean up using BeautifulSoup
for page in data:
	if page['page_content'] != None:
		text = page['page_content']
		text_temp = None
		# Loop to remove nested tags
		while text != text_temp:
			text_temp = text
			soup = BeautifulSoup(text_temp, 'html.parser')
			text = soup.get_text()
		page['page_content'] = text
	else:
		print('Error')

# Extraction of keys
keys = []
with open(file_in) as csvfile:
	reader = csv.reader(csvfile)
	keys = next(reader)

# Writing into output file
with open(file_out, 'w') as csvfile:
	dict_writer = csv.DictWriter(csvfile, keys)
	dict_writer.writeheader()
	dict_writer.writerows(data)