import string

class IndexedWord:
	def __init__(self, word):
		self.word = word
		self.totalCount = 0
		self.sequentialDocumentIds = []
		self.lastDocId = None

	def addDocId(self, newDocId):
		docIdToAdd = newDocId
		if self.lastDocId:
			if newDocId == self.lastDocId:
				return
			docIdToAdd -= self.lastDocId
		self.sequentialDocumentIds.append([docIdToAdd, 0])
		self.lastDocId = newDocId

	def wordOccured(self, docId):
		self.addDocId(docId)
		self.totalCount += 1
		self.sequentialDocumentIds[len(self.sequentialDocumentIds) - 1][1] += 1

class IndexedWordList:
	def __init__(self):
		self.inedexedWordList = []
		self.docWordCountList = []

	def addWordToListWithDocId(self, word, docId):
		if len(self.docWordCountList) < docId:
			self.docWordCountList.append(0)
		self.docWordCountList[docId - 1] += 1
		# Binary Search on list to see where the word would be
		wordIndex = self.getWordIndexInList(word)
		if wordIndex < len(self.inedexedWordList) and self.inedexedWordList[wordIndex].word == word:
			self.inedexedWordList[wordIndex].wordOccured(docId)
		else:
			newWord = IndexedWord(word)
			newWord.wordOccured(docId)
			self.inedexedWordList.insert(wordIndex, newWord)

	def getWordIndexInList(self, word):
		if len(self.inedexedWordList) < 1:
			return 0
		return self.binarySearchForWordIndex(word, 0, len(self.inedexedWordList) - 1)

	def binarySearchForWordIndex(self, word, low, high):
		if high - low < 2:
			for wordIndex in range(low, high + 1):
				if self.inedexedWordList[wordIndex].word >= word:
					return wordIndex
			return high + 1
		mid = (high - low) / 2 + low
		if self.inedexedWordList[mid].word == word:
			return mid
		elif self.inedexedWordList[mid].word < word:
			return self.binarySearchForWordIndex(word, mid, high)
		else:
			return self.binarySearchForWordIndex(word, low, mid)

	def printWordList(self):
		for indexedWord in self.inedexedWordList:
			print indexedWord.word, indexedWord.sequentialDocumentIds

class Reader:
	def __init__(self):
		self.dict = IndexedWordList()
		self.documentIdToNumList = []
		self.currentDocNum = 0

	def addDocIdToList(self, docId):
		self.documentIdToNumList.append(docId)

	def addWordsToDict(self, words):
		for word in words:
			self.dict.addWordToListWithDocId(word, self.currentDocNum)

	def getWordsFromText(self, text):
		text = text.translate(None, string.punctuation)
		return text.lower().split(' ')

	def getWordsFromDoc(self, doc):
		for line in f:
			if line.startswith("<P>"):
				self.addWordsToDict(self.getWordsFromText(line.replace("<P>", "").replace("</P>","").replace("\n","")))
		self.dict.printWordList()
		print self.dict.docWordCountList

	def parseDoc(self, doc):
		for line in f:
			if line.startswith("<DOCID>"):
				self.addDocIdToList(line.replace("<DOCID>", "").replace("</DOCID>", ""))
				self.currentDocNum += 1
			elif line.startswith("<P>"):
				wordsFromDoc = self.getWordsFromText(line.replace("<P>", "").replace("</P>","").replace("\n",""))
				self.addWordsToDict(wordsFromDoc)
		self.dict.printWordList()
		print self.dict.docWordCountList

f = open('example.xml', 'r')
reader = Reader()
reader.parseDoc(f)

f = open('myfile', 'w')
f.write('hi there\n')
f.close()