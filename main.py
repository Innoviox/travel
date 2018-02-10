#https://uwecuserletrabwn.files.wordpress.com/2011/12/ex2-reference-map-ifinal.jpg
#sub:
    #purple -> green
    #yellow -> yellow
    #green -> red
    #blue -> blue
import gui

bag = gui.parse.createBag()
gui.random.shuffle(bag)
r1 = []
r2 = []
dC = []

while True:
    for (i, r) in enumerate([r1, r2]):
        gui.gui(dC, bag, r)
        globals()['r'+str(i+1)] = gui.r
        dC = gui.dp.cardsIn[:]
        bag = gui.d.cardsIn
        if gui.won:
            raise SystemExit
