#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None # We see this as distance vector for this router

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")
        self.myGUI.println("Running init for router {}".format(self.myID))
        self.costs = deepcopy(costs)
        self.neighborsCosts = {} # Direct cost to my neighbors
        self.distanceVectors = {self.myID: self.costs} # Contains my and my neighbors costs
        self.nextRouter = {} # A dictionary which contains next router to each destination 
        
        self.myGUI.println("Costs is: {}".format(self.costs))

        # A dictionary for saving neighbors and corresponding cost
        for i in range(len(self.sim.connectcosts)):
            if i == self.myID:
                for j in range(len(self.sim.connectcosts)):
                    if self.sim.connectcosts[i][j] != sim.INFINITY and self.sim.connectcosts[i][j] != 0:
                        self.neighborsCosts[j] = self.sim.connectcosts[i][j]
                break
            
        # Building distanceVectors containing my and my neighbors distance vector
        for neighbor in self.neighborsCosts:
            self.distanceVectors[neighbor] = []
            for node in range(self.sim.NUM_NODES):
                if node == neighbor:
                    self.distanceVectors[neighbor].append(0)
                else:
                    self.distanceVectors[neighbor].append(self.sim.INFINITY)
                    
        self.myGUI.println("Distance vectors in router {} is.".format(self.myID))
        for i in sorted(self.distanceVectors):
            self.myGUI.println( str(i) + " : " + str(self.distanceVectors[i]))

        # Finds next router for every destination. If destination is not known yet it is '-' for now.
        for i in range(self.sim.NUM_NODES):
            if i in self.neighborsCosts and i != self.myID:
                self.nextRouter[i] = i
            else:
                self.nextRouter[i] = '-'
    
        # Sending updates to neighbors after initializing
        for n in self.neighborsCosts:
            pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
            self.myGUI.println("Sending distance vector from router {} which is ({}) to router {}".format(self.myID, self.costs, n))
            self.sendUpdate(pkt)
        
    # --------------------------------------------------
    # Receiving the updates and calculating after that
    def recvUpdate(self, pkt):
        self.myGUI.println("Router {} is receiving {} from router {}".format(self.myID, pkt.mincost, pkt.sourceid))
        self.distanceVectors[pkt.sourceid] = pkt.mincost # Routers distance vector updates with new costs of its neighbor
        self.calculate()

    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

    # --------------------------------------------------
    def printDistanceTabl#!/usr/bin/env python import GuiTextArea, RouterPacket, F from copy import deepcopy  class RouterNode():     myID = None     myGUI = None     sim = None     costs = None # We see this as distance vector for this router      # --------------------------------------------------     def __init__(self, ID, sim, costs):         self.myID = ID         self.sim = sim         self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")         self.myGUI.println("Running init for router {}".format(self.myID))         self.costs = deepcopy(costs)         self.neighborsCosts = {} # Direct cost to my neighbors         self.distanceVectors = {self.myID: self.costs} # Contains my and my neighbors costs         self.nextRouter = {} # A dictionary which contains next router to each destination                   self.myGUI.println("Costs is: {}".format(self.costs))          # A dictionary for saving neighbors and corresponding cost         for i in range(len(self.sim.connectcosts)):             if i == self.myID:                 for j in range(len(self.sim.connectcosts)):                     if self.sim.connectcosts[i][j] != sim.INFINITY and self.sim.connectcosts[i][j] != 0:                         self.neighborsCosts[j] = self.sim.connectcosts[i][j]                 break                      # Building distanceVectors containing my and my neighbors distance vector         for neighbor in self.neighborsCosts:             self.distanceVectors[neighbor] = []             for node in range(self.sim.NUM_NODES):                 if node == neighbor:                     self.distanceVectors[neighbor].append(0)                 else:                     self.distanceVectors[neighbor].append(self.sim.INFINITY)                              self.myGUI.println("Distance vectors in router {} is.".format(self.myID))         for i in sorted(self.distanceVectors):             self.myGUI.println( str(i) + " : " + str(self.distanceVectors[i]))          # Finds next router for every destination. If destination is not known yet it is '-' for now.         for i in range(self.sim.NUM_NODES):             if i in self.neighborsCosts and i != self.myID:                 self.nextRouter[i] = i             else:                 self.nextRouter[i] = '-'              # Sending updates to neighbors after initializing         for n in self.neighborsCosts:             pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))             self.myGUI.println("Sending distance vector from router {} which is ({}) to router {}".format(self.myID, self.costs, n))             self.sendUpdate(pkt)              # --------------------------------------------------     # Receiving the updates and calculating after that     def recvUpdate(self, pkt):         self.myGUI.println("Router {} is receiving {} from router {}".format(self.myID, pkt.mincost, pkt.sourceid))         self.distanceVectors[pkt.sourceid] = pkt.mincost # Routers distance vector updates with new costs of its neighbor         self.calculate()      # --------------------------------------------------     def sendUpdate(self, pkt):         self.sim.toLayer2(pkt)      # --------------------------------------------------     def printDistanceTable(self):         self.myGUI.println("Current table for " + str(self.myID) +                            "  at time " + str(self.sim.getClocktime()))                  self.myGUI.println("\nDistancetable:")         # Printing first line of distance table         headerStr = "    dst |"         for i in range(self.sim.NUM_NODES):             headerStr += " " * 5 + str(i)         headerStr += "\n" + "-" * len(headerStr)         self.myGUI.println(headerStr)                  # Printing neighbors and corresponding cost in table         # Each iteration is one neighbor         for neighbor in self.neighborsCosts:             self.myGUI.print(" nbr {}  |".format( neighbor))             for i in self.distanceVectors[neighbor]:                  self.myGUI.print("{:>6}".format(i))             self.myGUI.println()          self.myGUI.println("\nOur distance vector and routes:")          # Printing first line of our distance vector and routes         headerStr = "    dst |"         for i in range(self.sim.NUM_NODES):             headerStr += " " * 5 + str(i)         headerStr += "\n" + "-" * len(headerStr)         self.myGUI.println(headerStr)                  # Printing the cost line         self.myGUI.print(" cost   |")         for i in range(self.sim.NUM_NODES):             self.myGUI.print("{:>6}".format(self.costs[i]))          # Printing the route line, which is the next router         self.myGUI.println()         self.myGUI.print(" route  |")         for i in range(self.sim.NUM_NODES):             self.myGUI.print("{:>6}".format(self.nextRouter[i]))         self.myGUI.println()             # --------------------------------------------------     def updateLinkCost(self, dest, newcost):         self.myGUI.println("updateLink called from router {}\n{}".format(self.myID, "*" * 30))         self.myGUI.println("Destination is {} and the new cost is {}".format(dest, newcost))         self.neighborsCosts[dest] = newcost          # If -p True then it will imagine that any other nighbors that are going through myself to         # destination have an infinite cost to prevent count-to-infinity problem         if self.sim.POISONREVERSE:              for neighbor in self.neighborsCosts:                  if neighbor != dest and self.sim.nodes[neighbor].nextRouter[dest] == self.myID:                      self.distanceVectors[neighbor][dest] = self.sim.INFINITY          self.calculate()              # --------------------------------------------------     def calculate(self):         self.myGUI.println("Calculating...")          self.myGUI.println("Distance vectors in router {} is.".format(self.myID))         for i in sorted(self.distanceVectors):             self.myGUI.println( str(i) + " : " + str(self.distanceVectors[i]))          self.myGUI.println("NeighborsCosts is: {}".format(str(self.neighborsCosts)))          changed = False          # Bellman-Ford equation         for n in range(self.sim.NUM_NODES):             if n == self.myID:                 continue              # We will find a minimum cost to each destination using this equation: "Dx(n) = min v {c(x,v) + Dv(n)}"             mincost = self.sim.INFINITY             for neighbor in self.neighborsCosts:                 if self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n] < mincost:                     mincost = self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n]                     self.nextRouter[n] = neighbor              # If there is some difference update the costs for this destination              if self.costs[n] != mincost:                 self.costs[n] = mincost                 changed = True                          # If there is any difference from last costs we should inform it to our neighbors         if changed:             self.myGUI.println("Distance vector changed for router {} and now is {}.".format(self.myID, self.costs))             for n in self.neighborsCosts:                 pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))                 self.myGUI.println("Sending distance vector from router {} to router {}".format(self.myID, n))                 self.sendUpdate(pkt)         else:             self.myGUI.println("Distance vector DID NOT change for router {}.".format(self.myID))
        self.myGUI.println("\nDistancetable:")
        # Printing first line of distance table
        headerStr = "    dst |"
        for i in range(self.sim.NUM_NODES):
            headerStr += " " * 5 + str(i)
        headerStr += "\n" + "-" * len(headerStr)
        self.myGUI.println(headerStr)
        
        # Printing neighbors and corresponding cost in table
        # Each iteration is one neighbor
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
        
        # Printing the cost line
        self.myGUI.print(" cost   |")
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("{:>6}".format(self.costs[i]))

        # Printing the route line, which is the next router
        self.myGUI.println()
        self.myGUI.print(" route  |")
        for i in range(self.sim.NUM_NODES):
            self.myGUI.print("{:>6}".format(self.nextRouter[i]))
        self.myGUI.println()
       
    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        self.myGUI.println("updateLink called from router {}\n{}".format(self.myID, "*" * 30))
        self.myGUI.println("Destination is {} and the new cost is {}".format(dest, newcost))
        self.neighborsCosts[dest] = newcost

        # If -p True then it will imagine that any other nighbors that are going through myself to
        # destination have an infinite cost to prevent count-to-infinity problem
        if self.sim.POISONREVERSE:
             for neighbor in self.neighborsCosts:
                 if neighbor != dest and self.sim.nodes[neighbor].nextRouter[dest] == self.myID:
                     self.distanceVectors[neighbor][dest] = self.sim.INFINITY

        self.calculate()
        
    # --------------------------------------------------
    def calculate(self):
        self.myGUI.println("Calculating...")

        self.myGUI.println("Distance vectors in router {} is.".format(self.myID))
        for i in sorted(self.distanceVectors):
            self.myGUI.println( str(i) + " : " + str(self.distanceVectors[i]))

        self.myGUI.println("NeighborsCosts is: {}".format(str(self.neighborsCosts)))

        changed = False

        # Bellman-Ford equation
        for n in range(self.sim.NUM_NODES):
            if n == self.myID:
                continue

            # We will find a minimum cost to each destination using this equation: "Dx(n) = min v {c(x,v) + Dv(n)}"
            mincost = self.sim.INFINITY
            for neighbor in self.neighborsCosts:
                if self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n] < mincost:
                    mincost = self.neighborsCosts[neighbor] + self.distanceVectors[neighbor][n]
                    self.nextRouter[n] = neighbor

            # If there is some difference update the costs for this destination 
            if self.costs[n] != mincost:
                self.costs[n] = mincost
                changed = True
                
        # If there is any difference from last costs we should inform it to our neighbors
        if changed:
            self.myGUI.println("Distance vector changed for router {} and now is {}.".format(self.myID, self.costs))
            for n in self.neighborsCosts:
                pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
                self.myGUI.println("Sending distance vector from router {} to router {}".format(self.myID, n))
                self.sendUpdate(pkt)
        else:
            self.myGUI.println("Distance vector DID NOT change for router {}.".format(self.myID))