#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None # We see this as distance vector for this router

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs): # 
        self.myID = ID
        print("Running init for router {}".format(self.myID))
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")
        self.costs = deepcopy(costs)
        self.orgCosts = deepcopy(costs)
        self.neighborsCosts = {} # EX: {1:4, 2:1} c(x,y)
       # self.neighbors = []
        self.distanceVectors = {self.myID: self.costs}
        self.nextRouter = {}
        self.routingTable = []
        
        print("Costs is:" , self.costs)

        # a dictionary for saving neighbors and corresponding cost
        for i in range(len(self.sim.connectcosts)):
            if i == self.myID:
                for j in range(len(self.sim.connectcosts)):
                    if self.sim.connectcosts[i][j] != sim.INFINITY and self.sim.connectcosts[i][j] != 0:
                        self.neighborsCosts[j] = self.sim.connectcosts[i][j]
                break
            

        # Finding directly attached neighbors
        # for i in range(len(self.sim.connectcosts)):
        #     if i == self.myID:
        #         for j in range(len(self.sim.connectcosts)):
        #             if self.sim.connectcosts[i][j] != sim.INFINITY and self.sim.connectcosts[i][j] != 0:
        #                 self.neighbors.append(j)
        #         break
            
        # Building distanceVectors containing my and my neighbors distance vector
        for neighbor in self.neighborsCosts:
            self.distanceVectors[neighbor] = []
            for node in range(self.sim.NUM_NODES):
                self.distanceVectors[neighbor].append(self.sim.INFINITY)
            
        print(self.distanceVectors)

        # Building routing table
        # for i in range(self.sim.NUM_NODES):
        #     if i == self.myID:
        #         self.routingTable.append(self.costs)
        #         continue
        #     temp_list = []
        #     for j in range(self.sim.NUM_NODES):
        #         temp_list.append(self.sim.INFINITY)

        #     self.routingTable.append(temp_list)
            
        # print("This is routingTable for router {}".format(self.myID))
        # print(self.routingTable)
        
        for i in range(self.sim.NUM_NODES):
            if i in self.neighborsCosts and i != self.myID:
                #print("{} Finns i {}.".format(i, self.neighborsCosts))
                self.nextRouter[i] = i
            else:
                self.nextRouter[i] = '-'
                

        # Sending updates.
        for n in self.neighborsCosts:
            pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
            print("Sending distance vector from router {} which is ({}) to router {}".format(self.myID, self.costs, n))
            self.sendUpdate(pkt)
        
    # --------------------------------------------------
    def recvUpdate(self, pkt):
        print("recvUpdate called from router {} from router {}!".format(self.myID, pkt.sourceid))

        self.distanceVectors[pkt.sourceid] = pkt.mincost
        self.calculate()

    # --------------------------------------------------
    def sendUpdate(self, pkt):
       # print("sendUpdate called from router {}!".format(self.myID))
        self.sim.toLayer2(pkt)

    # --------------------------------------------------
    def printDistanceTable(self):
        #print("PrintTable called from router {}".format(self.myID))
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        
        self.myGUI.println("\nDistancetable:")
        # Printing first line of distance table
        headerStr = "    dst |"
        for i in range(self.sim.NUM_NODES):
            headerStr += " " * 5 + str(i)
        headerStr += "\n" + "-" * len(headerStr)
        self.myGUI.println(headerStr)
        

        for neighbor in self.neighborsCosts:
            self.myGUI.print(" nbr {}  |".format( neighbor))
            for i in self.distanceVectors[neighbor]:
                 self.myGUI.print("{:>6}".format(i))
            self.myGUI.println()


        self.myGUI.println("\nOur distance vector and routes:")

        # Printing first line of our distance vector and routes
        headerStr = "    dst |"
        for i in range(self.sim.NUM_NODES):
            headerStr += " " * 5 + str(i)
        headerStr += "\n" + "-" * len(headerStr)
        self.myGUI.println(headerStr)
        
        self.myGUI.print(" cost   |")
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("{:>6}".format(self.costs[i]))

        self.myGUI.println()
        self.myGUI.print(" route  |")

        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("{:>6}".format(self.nextRouter[i]))
        self.myGUI.println()
       
    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        # print("updateLink called from router {}".format(self.myID))
        print(dest, newcost)

        self.costs[dest] = self.sim.INFINITY
        print(self.costs)
        self.neighborsCosts[dest] = newcost

        for n in self.neighborsCosts:
            pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
            print("Sending distance vector from router {} to router {}".format(self.myID, n))
            self.sendUpdate(pkt)


    # --------------------------------------------------
    # Works without linkcost-change.         
    # def calculate(self):
    #     print("Distance vectors in router {} is.".format(self.myID))
    #     for i in sorted(self.distanceVectors):
    #         print( str(i) + " : " + str(self.distanceVectors[i]))

    #     print("NeighborsCosts is: " , self.neighborsCosts)
    #     changed = False
    #     for n in range(self.sim.NUM_NODES):
    #         mincost = self.costs[n] # 10
    #         for neighbor in self.neighborsCosts:
    #             if self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n] < mincost:
    #                 changed = True
    #                 mincost = self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n]
    #                 self.nextRouter[n] = neighbor

    #         if changed:
    #             self.costs[n] = mincost

    #     if changed:
    #         print("Distance vector changed for router {} and now is {}.".format(self.myID, self.costs))
    #         for n in self.neighborsCosts:
    #             pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
    #             print("Sending distance vector from router {} to router {}".format(self.myID, n))
    #             self.sendUpdate(pkt)
    #     else:
    #         print("Distance vector DID NOT change for router {}.".format(self.myID))
    # --------------------------------------------------
    # New version. Works with linkcost-change on
    def calculate(self):
        print("Distance vectors in router {} is.".format(self.myID))
        for i in sorted(self.distanceVectors):
            print( str(i) + " : " + str(self.distanceVectors[i]))

        print("NeighborsCosts is: " , self.neighborsCosts)
        changed = False
        for n in range(self.sim.NUM_NODES):
            if n == self.myID:
                continue
            mincost = self.sim.INFINITY
            for neighbor in self.neighborsCosts:
                if self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n] < mincost:
                    mincost = self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n]
                    self.nextRouter[n] = neighbor

            if self.costs[n] != mincost:
                self.costs[n] = mincost
                changed = True

        if changed:
            print("Distance vector changed for router {} and now is {}.".format(self.myID, self.costs))
            for n in self.neighborsCosts:
                pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
                print("Sending distance vector from router {} to router {}".format(self.myID, n))
                self.sendUpdate(pkt)
        else:
            print("Distance vector DID NOT change for router {}.".format(self.myID))

        
if __name__ == "__main__":
    pass
 
