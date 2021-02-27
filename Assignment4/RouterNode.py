#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None
    nbr = []

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs): # 
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        self.costs = deepcopy(costs)
        self.nbr = []

        print("Running for router {} and len(nbr) is : {}".format(self.myID, len(self.nbr)))
        for i in range(len(sim.connectcosts)):
            print (self.sim.connectcosts[i])

        print("Done!")
        
        for i in range(len(self.sim.connectcosts)):
            if i == self.myID:
                for j in range(len(self.sim.connectcosts)):
                    if self.sim.connectcosts[i][j] != sim.INFINITY and self.sim.connectcosts[i][j] != 0:
                         if j not in self.nbr:
                             self.nbr.append(j)
                break

        for i in self.nbr:
            print(i)

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        print("recv called from router {} and I am recving from router {}!".format(self.myID, pkt.sourceid))
        
        self.costs[pkt.sourceid] = pkt.mincost[pkt.sourceid]
        
        # if pkt.sourceid not in self.nbr:
        #     self.nbr.append(pkt.sourceid)
        # print("my nbrs are: {}".format(self.nbr))
    # --------------------------------------------------
    def sendUpdate(self, pkt):
        print("send called from router {}!".format(self.myID))
        self.sim.toLayer2(pkt)

    # --------------------------------------------------
    def printDistanceTable(self):
        #print(self.costs)
        print("PrintTable called from router {}".format(self.myID))
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))

        self.myGUI.println("\nDistancetable:")
        headerStr = "    dst |"
        for i in range(len(self.costs)):
            headerStr += " " * 5 + str(i)
        headerStr += "\n" + "-" * len(headerStr)
        self.myGUI.println(headerStr)

        for i in self.nbr:
            self.myGUI.print(" nbr  " + str(i) + " |"+ "\n")
        

    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        print("updateLink called from router {}".format(self.myID))
        print(dest, newcost)
        self.costs[dest] = newcost
        print(self.costs)


        for n in self.nbr:
            pkt = RouterPacket.RouterPacket(self.myID, n, self.costs)
            print("Sending updates to router {}".format(n))
            self.sendUpdate(pkt)
        
    
if __name__ == "__main__":
    pass
 
