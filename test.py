#! /usr/bin/python

class classA():
    def __init__(self, csv = ""):
        print ("Inside classA init")

    def set_csv(self, csv):
        print( "Setting csv to %s" %csv)
        self.csv = csv

    def update_a(self,up):
        self.csv=up

class classB(classA):
    def __init__(self,csv):
        print("Inside classB init")
        classA.__init__(self, csv)
        classA.set_csv(self, csv)
        print( "class B csv after set_csv %s" %self.csv)
        self.csv=csv

    def printcsv(self):
        print( self.csv)
c_b = classB("abc")
c_b.update_a("not")
c_b.printcsv()

