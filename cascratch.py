from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import DragBehavior
from kivy.lang.builder import Builder
Builder.load_file('cascratch.kv')
def checkCollide(widget1,widget2):
	print('check started')
	if widget1.right > widget2.x and widget1.x < widget2.right and widget1.top > widget2.y and widget1.y < widget2.top:
		print("check success")
		return widget2.value

class mainLayout(ScatterLayout):
	def genpog(self):
		self.add_widget(Pog(center=self.ids['spot'].center))
	def betCheck(self):
		labels=['label1','label2']
		for each in labels:
			print('bet started')
			if type(checkCollide(Pog(),self.ids[each])) == int:
				print("The pog collided with {}".format(each))
class Pog(Scatter):
	pass
test=mainLayout(do_rotation=False, do_scale=False, do_translation=False)
class mainApp(App):
	def build(self):
		return test
main=mainApp()
main.run()