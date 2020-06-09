import os

os.chdir("C:/Users/victo/Documents/Hangman")

language = input("Chose language... (DE/EN) ")
if language == "DE" or language == "De" or language == "de":
	list = [line.strip("\n") for line in open("wordlist_de.txt", 'r', encoding='utf-8')]
elif language == "EN" or language == "En" or language == "en":
	list = [line.strip("\n") for line in open("wordlist_en.txt", 'r', encoding='utf-8')]

wordlist = [x.lower() for x in list]
already_guessed = []
num_guessed = 0

def find_char(list, already_guessed):
	count = [0] * 256

	max = -1
	c = ""

	for word in list:
		for i in word:
			count[ord(i)]+=1;
			for i in already_guessed:
				count[ord(i)] = 0

		for i in word:
			if max < count[ord(i)]:
				max = count[ord(i)]
				c=i

	return c

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

posibilities = len(wordlist)
print(posibilities)
wordlength = eval(input("Anzahl der Buchstaben: "))

newpos = []
count = 0
found = 0
for word in wordlist:
	if len(word) == wordlength:
		found += 1
		newpos.append(word)
	count += 1
	print("scanning... ", float("{0:.2f}".format(count/posibilities*100)), " percent done:", "found", found, "words", end="\r")

print("\n", "There are currently ", len(newpos), "posibilities...")

game = True

while game:
	print("\n", "There are currently ", len(newpos), "posibilities...")
	guess = find_char(newpos, already_guessed)
	question = input("Ist ein '" + guess + "' in ihrem Wort enthalten? (Ja/Nein) ")

	if question == "Ja" or question == "ja":
		num = eval(input("Wie oft? "))
		newpos = update_list_true(newpos, guess, num)
		already_guessed.append(guess)
		num_guessed += num
	elif question == "Nein" or question == "nein":
		newpos = update_list_false(newpos, guess)

	if num_guessed == wordlength:
		print("Es ist eins von diesen Wörtern: ", newpos)
		game = False
