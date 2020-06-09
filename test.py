wordlist = ["Hallo", "abfbr", "ssnfn", "jdk", "eerfg", "abnba"]

posibilities = len(wordlist)

wordlength = eval(input("sag: "))

newpos = []
count = 0
found = 0
for word in wordlist:
	if len(word) == wordlength:
		found += 1
		newpos.append(word)
	count += 1
	print("scanning... ", float("{0:.2f}".format(count/posibilities*100)), " percent done:", "found", found, "words", end="\r")

print(newpos)

def update_list_true(list, guess, num):

	newlist = []
	for word in list:
		number = word.count(guess)
		if number == num:
			newlist.append(word)

	return newlist

def update_list_false(list, guess):

	newlist=[]
	for word in list:
		number = word.count(guess)
		if number == 0:
			newlist.append(word)

	return newlist

frage = input("Ist ein 'a' in ihrem Wort enthalten")

if frage == "Ja":
	num = eval(input("Wie oft"))
	newlist=update_list_true(newpos, "a", num)
elif frage == "Nein":
	newlist = update_list_false(newpos, "a")

print(newlist)
