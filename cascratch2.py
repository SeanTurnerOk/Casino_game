from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang.builder import Builder
Builder.load_file('cascratch2.kv')

class mainLayout(BoxLayout):
	def populate(self):
		self.add_widget(NewLabel())
class mainThing(App):
	def build(self):
		return mainLayout()
main=mainThing()
main.run()