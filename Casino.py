from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
from random import randint
Builder.load_file('Casino.kv')
def checkCollide(widget1,widget2):
	if widget1.right > widget2.x and widget1.x < widget2.right and widget1.top > widget2.y and widget1.y < widget2.top:
		return widget2.value
	#While kivy does have a collide_widget function, it only returns a boolean of True or False. As such I made my own, and placed it outside of every function since it is a general use case
class Card():
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank= rank
	def img(self):
		return Image(source='card_img/{} of {}.png'.format(self.rank, self.suit))
	def __str__(self):
		return "{} of {}".format(self.rank, self.suit)
		#Cards initialized with both suit and rank, and an image is drawn from the folder card_img when the function img() is called in order to keep the size of the deck lower.
		#__str__ is here to show that I know how to use it, and format. It is not used.
class Deck():
	suits= ['Hearts', 'Diamonds', 'Spades', 'Clubs']
	ranks= [n for n in range(2,11)] + ['Jack', 'Queen', 'King', 'Ace']
	#suits and ranks are denoted here for easy mutability. If a new suit were needed, for some reason, then it would be simple to add it and all else would change with it
	def __init__(self):
		self.contents= []
		self.contents= [Card(suit, rank) for rank in self.ranks for suit in self.suits]
		self.graveyard=[]
		self.shuffle()
		#Actual cards generated and placed in self.contents, which is used to keep all decks from sharing the same contents and graveyard, were I to add another card game to the app.
		#self.shuffle is here as a catch-all, to ensure that, even if later in the code it is not shuffled again, there is at least one completely random set of draws. There should, however, be a .shuffle() call at each loading of a card game screen
	def __len__(self):
		return len(self.contents)
		#mostly used to tell when the deck is empty
	def shuffle(self, *args):
		if 'reshuffle' in args:
			self.contents+= self.graveyard
			self.graveyard=[]
		i=0
		r=0
		temp=Card('foo','bar')
		#A temporary card and value for r were generated to reserve memory space
		while i < len(self.contents):
			temp = self.contents[i]
			r= randint(0, len(self.contents)-1)
			self.contents[i]=self.contents[r]
			self.contents[r]=temp
			i+=1
			'''A less CPU intensive shuffling could easily be done by declaring an empty temp list, using 
					temp+= [self.contents.pop(randint(0, (len(self.contents)-1)))]
				and then assigning to self.contents the new temp list here, which has one assignment per loop instead of three, but memory space was considered more valuable.'''
	def draw(self):
		if len(self.contents)>0:
			return [self.contents.pop(0)]
		elif len(self.contents)==0 and len(self.graveyard)>0:
			self.shuffle('reshuffle')
			return [self.contents.pop(0)]
		else:
			raise NameError('No cards in deck')
		#Doing this keeps the Deck from ever having duplicates placed into it, as everything used is removed from it, and must be placed back in
	def discard(self, card):
		self.graveyard += [card]
	#An important note, all cards that need to be in the deck must be discarded back into the deck, or they will not be re-generated, to prevent card duplication.

class Hand():
	def __init__(self):
		self.contents=[]
	'''	def __str__(self):
			temp=''
			if len(self.contents)==0:
				return 'No cards in hand'
				#Mostly a debug message, may be used later.
			elif len(self.contents)==1:
				return 'A '+str(self.contents[0])+'.'
			elif len(self.contents)>1:
				i = 1
				for each in self.contents:
					if i == 1:
						temp += 'A '+str(each)+', '
					elif i == len(self.contents):
						temp += 'and a '+str(each)+'.'
					else:
						temp+= 'a '+str(each) + ', '
					i+=1
			return str(temp)
	'''
	#__str__ made during early testing, kept in case a non-graphic mode is requested.
	def __len__(self):
		return len(self.contents)
	def __iter__(self):
		for i in range(0, len(self.contents)):
			yield self.contents[i]
		#Generator was used to keep up efficiency
	def draw(self, deck, *args):
		if args:
			for i in range(args[0]):
				self.contents+= deck.draw()
		else:
			self.contents+= deck.draw()
		#Args is used here instead of requiring a value to allow the much more common single card draw to be done without adding additional typing, keeping the coder from continuously having to type draw(deck,1)
	def discard(self, deck, *args):
		if 'all' in args:
			for each in self.contents:
				deck.discard(each)
			self.contents=[]
		else:
			for each in args:
				if each in self.contents:
					deck.discard(self.contents.pop(self.content.index(each)))
				elif each not in self.contents and each != 'all':
					raise NameError('Discarded card was not in Hand')
		#Discard all is the only discard currently used, but I wished to have a more robust system, in case another card game were to require it.
class Pog(Scatter):
	pass

class startScreen(Screen):
	pass

class lobbyScreen(Screen):
	pass

class blackjackScreen(Screen):
	deck=Deck()
	yourHand=Hand()
	dealerHand=Hand()
	#Each card screen is initialized with its own deck, and the various hands, to keep variables from leaking between screens, were another card game added.
	def loadScreen(self):
		self.deck.shuffle()
		self.ids['dealerHand'].clear_widgets()
		self.ids['yourHand'].clear_widgets()
		self.ids['dealerHand'].add_widget(Label(text="Dealer's Hand"))
		self.ids['yourHand'].add_widget(Label(text="Your Hand"))
		#to keep from having five different events simultaneously enacted with a single entrance of the screen, I made one function, which did five things sequentially, and bound that to the screen enter.
	def populateHand(self, who):
		if who == 'dealer':
			i = 0
			self.ids['dealerHand'].clear_widgets()
			for each in self.dealerHand:
				if i == 0:
					i+=1
					self.ids['dealerHand'].add_widget(Image(source='card_img/card backing.png'))
				else:
					self.ids['dealerHand'].add_widget(each.img())
				#The first card of the dealer's hand should be face down. The card itself is extant in exactly the same way as the others, but is not represented
		if who == 'your':
			self.ids['yourHand'].clear_widgets()
			for each in self.yourHand:
				self.ids['yourHand'].add_widget(each.img())
				#All cards should be represented on your hand, however.

	def jackValue(self, hand):
		score=0
		aceCount=0
		for each in hand.contents:
			if type(each.rank)==int:
				score += each.rank
			elif each.rank in ['Jack', 'Queen', 'King']:
				score +=10
			elif each.rank == 'Ace':
				aceCount+=1
			else:
				raise NameError('Card in deck not of correct format.') 
		score+= aceCount*11
		while score > 21 and aceCount > 0:
			aceCount -= 1
			score -= 10
			#This should allow you to have two aces and a nine, and still not be counted as having over 21 points.
		return score
	def dealerShow(self, hand):
		temp='?, '
		for each in hand.contents[1:]:
			temp+= str(each)
		return temp
	def checkWin(self, hand1, hand2, *args):
		def buttonUpdate(who):
			if who == 'dealer':
				self.ids['dealerHand'].add_widget(Label(text="Dealer Wins"))
			elif who == 'your':
				self.ids['yourHand'].add_widget(Label(text="You Win!"))
			self.buttonStates(True)
			#Method defined inside checkWin to keep it out of normal namespace, and because it is only ever able to be used in this specific instance
		self.populateHand('dealer')
		self.populateHand('your')
		if self.jackValue(hand1)>21:
			buttonUpdate('dealer')
		elif self.jackValue(hand2)>21 or len(hand1)>5:
			mainGame.money+= 3*mainGame.betAmount
			buttonUpdate('your')
		elif self.jackValue(hand1)==21:
			mainGame.money+= 3*mainGame.betAmount
			buttonUpdate('your')
		elif self.jackValue(hand2)==21:
			buttonUpdate('dealer')
		if 'stay' in args:
			if self.jackValue(hand1)>self.jackValue(hand2):
				mainGame.money+= 3*mainGame.betAmount
				buttonUpdate('your')
			else:
				buttonUpdate('your')
	def buttonStates(self, boolean):
		self.ids['stayButton'].disabled=boolean
		self.ids['drawButton'].disabled=boolean
		self.ids['betButton'].disabled=boolean
		#Method created for DRY principle

class rouletteScreen(Screen):
	pogHoard=[]
	#Generating a new instance of Pog() results in a widget that it is very difficult to reference to. A simple way to count all pogs is to just store a reference here
	result=0
	def generatePog(self):
		temp=Pog(pos=[self.ids['chipSpot'].center_x-(.5*self.ids['label1'].height), self.ids['chipSpot'].center_y-(.5*self.ids['label1'].height)], id='pog'+str(len(self.pogHoard)))
		self.pogHoard.append(temp)
		self.add_widget(temp)
	def betCheck(self):
		labels=[i for i in range(1,37)]
		gain=0
		for each in self.pogHoard:
			try:
				int(each.text)
			except:
				self.ids['resultLabel'].text="Try a real number, buddy!"
				return
			#Just a filter to ensure that the input on the chip is both extant and a number.
		for each in self.pogHoard:
			counter=0
			mainGame.money-=int(each.text)
			for i in labels:
				if type(checkCollide(each, self.ids["label"+str(i)])) == int and self.result == i:
					counter+=1
				#At the moment, the function checkCollide is not used for its intended purpose. When I figure out the graphical design for including 0, 00, Evens, and Odds, it will have much more utility, being able to distinguish between them by value.
			if counter == 1:
				gain = 50*int(each.text)
			elif counter == 2:
				gain = 25*int(each.text)
			elif counter==4:
				gain += 10*int(each.text)
			elif counter >4:
				self.ids['resultLabel'].text="error"
		if gain == 0:
			self.ids['resultLabel'].text="Better luck next time!"
		self.ids['winningLabel'].text = str(gain)
		mainGame.money+=gain
	def spinWheel(self):
		self.result = randint(1,36)
		self.ids['numberLabel'].text=('The winning number is {}'.format(str(self.result)))
		#A simple random number generator picks the winning number and updates the label. This was not built into the betCheck() method so it would be easier to debug, and be more understandable on the .kv side of things.

class betPopup(Popup):
	pass

gameManager=ScreenManager()
gameManager.add_widget(startScreen(name='Start'))
gameManager.add_widget(lobbyScreen(name='Lobby'))
gameManager.add_widget(blackjackScreen(name='Blackjack'))
gameManager.add_widget(rouletteScreen(name='Roulette'))
#Adding all Screens to the ScreenManager and giving them reference names.

class CasinoApp(App):
	betting=betPopup()
	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.money = 100
		self.betAmount = 0
		#Having self.money and self.betAmount outside would result in these being un-updatable constants, and the super just pulls all arguments from the original __init__ so the thing actually works

	def changeMoney(self, amount):
		self.money += amount
	def checkMoney(self):
		return int(self.money)
	def changeBet(self, amount):
		self.betAmount = amount
	def checkBet(self):
		return int(self.betAmount)
	#These could probably be done away with, but I have had issues with kivy in the past refusing to read variables attached to the main class, so I typically use methods like this.
	def build(self):
		return gameManager
		#returns the screenManager as the main display, which will display the first screen added to it, and will handle transitions from there.
mainGame= CasinoApp()
if __name__ == "__main__":
	mainGame.run()