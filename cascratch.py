from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import DragBehavior
from kivy.lang.builder import Builder
Builder.load_file('cascratch.kv')
def checkCollide(widget1,widget2):
	print('check started')
	if all([widget1.right > widget2.x, widget1.x < widget2.right, widget1.top > widget2.y, widget1.y < widget2.top]):
		print("check success")
		return widget2.value

class mainLayout(ScatterLayout):
	pogHoard=[]
	def genpog(self):
		temp=Pog(center=self.ids['spot'].center, id='pog'+str(len(self.pogHoard)))
		self.pogHoard.append(temp)
		self.add_widget(temp)
	def betCheck(self):
		labels=['label1','label2']
		for each in self.pogHoard:
			for i in labels:
				if type(checkCollide(each, self.ids[i])) == int:
					print('The pog collided with {}'.format(i))
class Pog(Scatter):
	pass
test=mainLayout(do_rotation=False, do_scale=False, do_translation=False)
class mainApp(App):
	def build(self):
		return test
main=mainApp()
main.run()