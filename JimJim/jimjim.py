#!/usr/bin/python

import wx
import libov2
import libitn
import libdownload
import os
import sys
import datetime
import subprocess

def getStaticURL(lat, long):
		return str('http://maps.google.com/staticmap?center=%s,%s&zoom=14&size=512x512&maptype=mobile&markers=%s,%s,bluep&sensor=false&key=ABQIAAAAzr2EBOXUKnm_jVnk0OJI7xSsTL4WIgxhMZ0ZK_kHjwHeQuOD4xQJpBVbSrqNn69S6DOTv203MQ5ufA' % (lat,long,lat,long))
		
def listFiles(dirname, suffix):
	fileset = set()
	for filename in os.listdir(dirname):
		fileSuffix = filename.upper()[0-len(suffix):]
		if fileSuffix == suffix.upper():
			fileset.add(os.path.join(dirname,filename))
	return fileset

class engine:
        poimap = dict()
	routemap = dict()

	tomtomdir = os.getcwd()

	EPHEMERAL_DATA_VALID = 1
	EPHEMERAL_DATA_MISSING = 2
	EPHEMERAL_DATA_EXPIRED = 3
	ephemeralMetaFile = 'ee_meta.txt'
	ephemeralExpires = datetime.datetime.utcnow()
	
        def __init__(self):
		self.parseEphemeralMetaFile()

	def getTomTomDir(self):
		return self.tomtomdir

	def setTomTomDir(self, dir):
		self.tomtomdir = dir
		self.parseEphemeralMetaFile()

	def parseEphemeralMetaFile(self):
		metaFile = os.path.join(self.tomtomdir,'ephem',self.ephemeralMetaFile)
		if os.path.exists(metaFile):
			f = open(metaFile,'r')
			self.ephemeralExpires = datetime.datetime.utcfromtimestamp(float(f.readline().split('=')[1]))
			if self.ephemeralExpires < datetime.datetime.utcnow():
				self.ephemeralValidity = self.EPHEMERAL_DATA_EXPIRED
			else:
				self.ephemeralValidity = self.EPHEMERAL_DATA_VALID
		else:
			self.ephemeralValidity = self.EPHEMERAL_DATA_MISSING

        #categoryname - the category name of this poiset
        #poiset - a set of lists each with the following format:  (NAME, LAT, LONG)
        #          [ (NAME0, LAT0, LONG0) , (NAME1, LAT1, LONG1) , ... ]
        def addPOIs(self, categoryname, poiset):
		if categoryname in self.poimap:
			self.poimap[categoryname].update(poiset)
		else:
                	self.poimap[categoryname] = poiset

	def getPOIs(self, categoryname):
		return self.poimap[categoryname]

	def removePOIs(self, categoryname):
                del self.poimap[categoryname]

        #routename - the name of this route
	#route - an ordered list of waypoints following the format: (LAT, LONG, NAME, TYPE)
	# TYPE is an integer representing:
	#	0 : An already visited destination
	#	1 : A waypoint
	#	2 : A destination yet to visit
	def addRoute(self, routename, route):
		self.routemap[routename] = route

	def getRoute(self, routename):
		return self.routemap[routename]

	def removeRoute(self, routename):
		del self.routemap[routename]

        #filename - the name of the directory to write files to files will be created for each
	#category e.g. (category.ov2)
        #def createFiles(self, dir):
        #        if len(self.poimap) > 0:
	#		for category in self.poimap:
	#			filename = os.path.join(dir,category+'.ov2')
	#			count = writeOV2(self.poimap[category],filename)
        #                	print ("%s POIs added to %s" % (count,filename))
        #        else:
        #                print ("No POIs added")

	def routes(self):
		return self.routemap.keys()

	def categories(self):
		return self.poimap.keys()

	def getQuickGPSValidity(self):
		return self.ephemeralValidity

	def getQuickGPSExpiry(self):
		return self.ephemeralExpires

	def downloadQuickGPS(self):
		if os.path.exists('quickgps.url'):
			f = open('quickgps.url','r')
			url = f.readline()
			destination = os.path.join(self.tomtomdir,'ephemeral.cab')
			libdownload.download(url,destination)
			subprocess.call(['cabextract','-d',self.tomtomdir,destination])
			self.parseEphemeralMetaFile()
		else:
			print "No quickgps.url"
	
class ITNEdit(wx.Dialog):
        def __init__(self, parent, id, waypoint):
                wx.Dialog.__init__(self, parent, id, "Edit Route", size=(400, 150))

                self.waypointRecord = (waypoint[0], waypoint[1], waypoint[2], waypoint[3])
                
                topPanel = wx.Panel(self, -1)
                panelSizer = wx.BoxSizer(wx.VERTICAL)
                topPanel.SetSizer(panelSizer)

                coordPanel = wx.Panel(topPanel, -1)
                coordSizer = wx.BoxSizer(wx.HORIZONTAL)
                coordPanel.SetSizer(coordSizer)
                panelSizer.Add(coordPanel, 1, wx.EXPAND, 0)

                latLabel = wx.StaticText(coordPanel, -1, "Latitude", (-1, -1), style=wx.ALIGN_LEFT)
                coordSizer.Add(latLabel, 0, wx.EXPAND | wx.ALL, 6)
                self.lat = wx.TextCtrl(coordPanel, -1, str(waypoint[0]), size=(-1, -1), style=wx.TE_LEFT)
                coordSizer.Add(self.lat, 1, wx.EXPAND | wx.ALL, 6)
                longLabel = wx.StaticText(coordPanel, -1, "Longitude", (-1, -1), style=wx.ALIGN_LEFT)
                coordSizer.Add(longLabel, 0, wx.EXPAND | wx.ALL, 6)
                self.long = wx.TextCtrl(coordPanel, -1, str(waypoint[1]), size=(-1, -1), style=wx.TE_LEFT)
                coordSizer.Add(self.long, 1, wx.EXPAND | wx.ALL, 6)

                self.name = wx.TextCtrl(topPanel, -1, waypoint[2], size=(-1, -1), style=wx.TE_MULTILINE)
                panelSizer.Add(self.name, 2, wx.EXPAND | wx.ALL, 6)

                buttonPanel = wx.Panel(topPanel, -1)
                buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
                buttonPanel.SetSizer(buttonSizer)
                panelSizer.Add(buttonPanel, 1, wx.EXPAND, 0)

                cancelButton = wx.Button(buttonPanel, wx.ID_CANCEL, '')
                cancelButton.Bind(wx.EVT_BUTTON, self.OnClose)
                buttonSizer.Add(cancelButton, 1, wx.EXPAND | wx.ALL, 6)
                okButton = wx.Button(buttonPanel, wx.ID_OK, '')
                okButton.Bind(wx.EVT_BUTTON, self.Update)
                buttonSizer.Add(okButton, 1, wx.EXPAND | wx.ALL, 6)

                self.Centre()
                self.ShowModal()
                self.Destroy()

        def OnClose(self, event):
                self.Close(True)

        def Update(self, event):
                self.waypointRecord = (float(self.lat.GetValue()), float(self.long.GetValue()), self.name.GetValue(), self.waypointRecord[3])
                self.Close(True)

        def GetRecord(self):
                return self.waypointRecord

class POIEdit(wx.Dialog):

        def __init__(self, parent, id, poiRow):
                wx.Dialog.__init__(self, parent, id, "Edit Point", size=(400, 170))

                self.poiRecord = (poiRow[0], poiRow[1], poiRow[2])
                
                topPanel = wx.Panel(self, -1)
                panelSizer = wx.BoxSizer(wx.VERTICAL)
                topPanel.SetSizer(panelSizer)

                coordPanel = wx.Panel(topPanel, -1)
                coordSizer = wx.BoxSizer(wx.HORIZONTAL)
                coordPanel.SetSizer(coordSizer)
                panelSizer.Add(coordPanel, 1, wx.EXPAND, 0)

                latLabel = wx.StaticText(coordPanel, -1, "Latitude", (-1, -1), style=wx.ALIGN_LEFT)
                coordSizer.Add(latLabel, 0, wx.EXPAND | wx.ALL, 6)
                self.lat = wx.TextCtrl(coordPanel, -1, str(poiRow[1]), size=(-1, -1), style=wx.TE_LEFT)
                coordSizer.Add(self.lat, 1, wx.EXPAND | wx.ALL, 6)
                longLabel = wx.StaticText(coordPanel, -1, "Longitude", (-1, -1), style=wx.ALIGN_LEFT)
                coordSizer.Add(longLabel, 0, wx.EXPAND | wx.ALL, 6)
                self.long = wx.TextCtrl(coordPanel, -1, str(poiRow[2]), size=(-1, -1), style=wx.TE_LEFT)
                coordSizer.Add(self.long, 1, wx.EXPAND | wx.ALL, 6)

		urlString = getStaticURL(poiRow[1],poiRow[2])
		urlText = wx.HyperlinkCtrl(topPanel, -1, 'View on Google Maps', urlString, (-1,-1))
		panelSizer.Add(urlText, 0, wx.EXPAND, 0)

                self.name = wx.TextCtrl(topPanel, -1, poiRow[0], size=(-1, -1), style=wx.TE_MULTILINE)
                panelSizer.Add(self.name, 2, wx.EXPAND | wx.ALL, 6)

                buttonPanel = wx.Panel(topPanel, -1)
                buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
                buttonPanel.SetSizer(buttonSizer)
                panelSizer.Add(buttonPanel, 1, wx.EXPAND, 0)

                cancelButton = wx.Button(buttonPanel, wx.ID_CANCEL, '')
                cancelButton.Bind(wx.EVT_BUTTON, self.OnClose)
                buttonSizer.Add(cancelButton, 1, wx.EXPAND | wx.ALL, 6)
                okButton = wx.Button(buttonPanel, wx.ID_OK, '')
                okButton.Bind(wx.EVT_BUTTON, self.Update)
                buttonSizer.Add(okButton, 1, wx.EXPAND | wx.ALL, 6)

                self.Centre()
                self.ShowModal()
                self.Destroy()

        def OnClose(self, event):
                self.Close(True)

        def Update(self, event):
                self.poiRecord = (self.name.GetValue(), float(self.lat.GetValue()), float(self.long.GetValue()))
                self.Close(True)

        def GetRecord(self):
                return self.poiRecord
                
class POIFrame(wx.Frame):
        ID_MENU_EXIT  = 101 
        ID_MENU_EXPORT_ALL_OV2 = 102
        ID_MENU_SET_MAP_DIR = 103

        ID_MENU_EDIT_POI = 201
        ID_MENU_IMPORT_OV2 = 202
	ID_MENU_MERGE_OV2 = 203
        ID_MENU_EXPORT_OV2 = 204
	ID_MENU_REMOVE_CAT = 205

        ID_MENU_EDIT_WAYPOINT = 301
        ID_MENU_IMPORT_ITN = 302
        ID_MENU_EXPORT_ITN = 303

        ID_MENU_ABOUT = 901

        ID_WIDGET_SECTIONLIST = 401

        ID_WIDGET_POICATLIST = 501 
        ID_WIDGET_POILIST = 502 

        ID_WIDGET_ITNCATLIST = 601 
        ID_WIDGET_ITNLIST = 602 
	
	ID_BUTTON_UPDATE_QUICKGPS = 701
	ID_BUTTON_CHANGE_LOCATION = 702

        data = engine()

        def __init__(self, parent, ID, title):
                wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(700, 500))

                ## Status Bar
                self.CreateStatusBar()
                self.SetStatusText("Ready")

                ## Menu Bar
                menuBar = wx.MenuBar()
                self.SetMenuBar(menuBar)
                             
                fileMenu = wx.Menu()
                fileMenu.Append(self.ID_MENU_SET_MAP_DIR, "Set &Map Location", "Set the map folder location on your TomTom device")
                wx.EVT_MENU(self, self.ID_MENU_SET_MAP_DIR, self.setmapdirGUI)

                fileMenu.Append(self.ID_MENU_EXPORT_ALL_OV2, "&Save", "Export all ov2 files to map folder")
                #wx.EVT_MENU(self, self.ID_MENU_EXPORT_ALL_OV2, self.exportov2files)

                fileMenu.AppendSeparator()

                fileMenu.Append(self.ID_MENU_EXIT, "E&xit", "Terminate the program")
                wx.EVT_MENU(self, self.ID_MENU_EXIT,  self.exit)

                menuBar.Append(fileMenu, "&File")

                ## Section Selection Widget
                topPanel = wx.Panel(self)
		self.guiSectionNotebook = wx.Notebook(topPanel, style=wx.NB_TOP)

		topSizer = wx.BoxSizer(wx.VERTICAL)
		topSizer.Add(self.guiSectionNotebook, 1, wx.EXPAND, 0)
		topPanel.SetSizer(topSizer)

                ## GPS Panel
                gpsMenu = wx.Menu()
                menuBar.Append(gpsMenu, "&GPS")
                
                gpsPanel = wx.Panel(self.guiSectionNotebook, -1)
		self.guiSectionNotebook.AddPage(gpsPanel, "My SatNav")

                gpsSizer = wx.BoxSizer(wx.VERTICAL)
                gpsPanel.SetSizer(gpsSizer)

                self.gpsLabel = wx.StaticText(gpsPanel, -1, '', (-1, -1), style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
                gpsSizer.Add(self.gpsLabel, 0, wx.EXPAND | wx.ALL, 4)

                self.gpsUpdateButton = wx.Button(gpsPanel, self.ID_BUTTON_UPDATE_QUICKGPS, 'Update')
                self.gpsUpdateButton.Bind(wx.EVT_BUTTON, self.downloadQuickGPS)
                gpsSizer.Add(self.gpsUpdateButton, 0, wx.ALIGN_CENTER | wx.ALL, 0)

		line2 = wx.StaticLine(gpsPanel, -1, (-1,-1), style=wx.LI_HORIZONTAL)
		gpsSizer.Add(line2, 0, wx.EXPAND | wx.ALL, 30)

		tomtomLocationTitleLabel = wx.StaticText(gpsPanel, -1, 'SatNav Location:', (-1, -1), style=wx.ALIGN_CENTRE)
		gpsSizer.Add(tomtomLocationTitleLabel, 0, wx.EXPAND | wx.ALL, 4)

		self.tomtomLocationLabel = wx.StaticText(gpsPanel, -1, '', (-1, -1), style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		gpsSizer.Add(self.tomtomLocationLabel, 0, wx.EXPAND | wx.ALL, 4)

                changeLocationButton = wx.Button(gpsPanel, self.ID_BUTTON_CHANGE_LOCATION, 'Change')
                changeLocationButton.Bind(wx.EVT_BUTTON, self.changeTomTomDirGUI)
                gpsSizer.Add(changeLocationButton, 0, wx.ALIGN_CENTER | wx.ALL, 0)

		line3 = wx.StaticLine(gpsPanel, -1, (-1,-1), style=wx.LI_HORIZONTAL)
		gpsSizer.Add(line3, 0, wx.EXPAND | wx.ALL, 30)

		self.updateGPSPanel()

                ## POI Panel
                poiMenu = wx.Menu()

                poiMenu.Append(self.ID_MENU_EDIT_POI, "&Edit", "Edit Selected POI")
                wx.EVT_MENU(self, self.ID_MENU_EDIT_POI, self.editpoi)
                
                poiMenu.AppendSeparator()
                
                poiMenu.Append(self.ID_MENU_IMPORT_OV2, "&Import OV2", "Import TomTom Overlay POI file as new category")
                wx.EVT_MENU(self, self.ID_MENU_IMPORT_OV2, self.importov2)

                poiMenu.Append(self.ID_MENU_MERGE_OV2, "&Merge OV2", "Import TomTom Overlay POI file into selected category")
                wx.EVT_MENU(self, self.ID_MENU_MERGE_OV2, self.mergeov2)

                poiMenu.AppendSeparator()

                poiMenu.Append(self.ID_MENU_EXPORT_OV2, "E&xport OV2", "Export selected category as TomTom Overlay file")
                wx.EVT_MENU(self, self.ID_MENU_EXPORT_OV2, self.exportov2)
                
                menuBar.Append(poiMenu, "&Poi")
                
                poiPanel = wx.Panel(self.guiSectionNotebook, -1)
		self.guiSectionNotebook.AddPage(poiPanel, "Points of Interest")
                poiPanel.Show(False)

                poiSizer = wx.BoxSizer(wx.HORIZONTAL)
                poiPanel.SetSizer(poiSizer)

                self.guiPOICatListBox = wx.ListBox(poiPanel, self.ID_WIDGET_POICATLIST, (-1, -1), (-1, -1), self.data.categories(), wx.LB_SINGLE | wx.LB_SORT)
                wx.EVT_LISTBOX(self, self.ID_WIDGET_POICATLIST, self.poiCatSelect)
                poiSizer.Add(self.guiPOICatListBox, 1, wx.EXPAND, 0)
                self.guiPOIListBox = wx.ListBox(poiPanel, self.ID_WIDGET_POILIST, (-1, -1), (-1, -1), (), wx.LB_SINGLE)
                wx.EVT_LISTBOX_DCLICK(self, self.ID_WIDGET_POILIST, self.editpoi)
                poiSizer.Add(self.guiPOIListBox, 2, wx.EXPAND | wx.LEFT, 4)

                ## ITN Panel
                itnMenu = wx.Menu()

                itnMenu.Append(self.ID_MENU_EDIT_WAYPOINT, "&Edit", "Edit Selected Waypoint")
                #wx.EVT_MENU(self, self.ID_MENU_EDIT_ITN, self.edititn)
                
                itnMenu.AppendSeparator()
                
                itnMenu.Append(self.ID_MENU_IMPORT_ITN, "&Import ITN", "Import TomTom ITN file")
                wx.EVT_MENU(self, self.ID_MENU_IMPORT_ITN, self.importitn)

                itnMenu.Append(self.ID_MENU_EXPORT_ITN, "E&xport ITN", "Export selected route as TomTom ITN file")
                wx.EVT_MENU(self, self.ID_MENU_EXPORT_ITN, self.exportitn)
                
                menuBar.Append(itnMenu, "&Routes")
                
                itnPanel = wx.Panel(self.guiSectionNotebook, -1)
		self.guiSectionNotebook.AddPage(itnPanel, "Routes")
                itnPanel.Show(False)

                itnSizer = wx.BoxSizer(wx.HORIZONTAL)
                itnPanel.SetSizer(itnSizer)

                self.guiITNCatListBox = wx.ListBox(itnPanel, self.ID_WIDGET_ITNCATLIST, (-1, -1), (-1, -1), self.data.categories(), wx.LB_SINGLE | wx.LB_SORT)
                wx.EVT_LISTBOX(self, self.ID_WIDGET_ITNCATLIST, self.itnCatSelect)
                itnSizer.Add(self.guiITNCatListBox, 1, wx.EXPAND, 0)
                self.guiITNListBox = wx.ListBox(itnPanel, self.ID_WIDGET_ITNLIST, (-1, -1), (-1, -1), (), wx.LB_SINGLE)
                wx.EVT_LISTBOX_DCLICK(self, self.ID_WIDGET_ITNLIST, self.edititn)
                itnSizer.Add(self.guiITNListBox, 2, wx.EXPAND | wx.LEFT, 4)
                
                ## About/Help Menu
                
                helpMenu = wx.Menu()
                helpMenu.Append(self.ID_MENU_ABOUT, "&About", "About the program")
                wx.EVT_MENU(self, self.ID_MENU_ABOUT, self.about)

                menuBar.Append(helpMenu, "&Help")

	def downloadQuickGPS(self,event):
		self.data.downloadQuickGPS()
		self.updateGPSPanel()

	def updateGPSPanel(self):
		quickGPSValidity = self.data.getQuickGPSValidity()
		self.gpsUpdateButton.Disable()
		if quickGPSValidity == self.data.EPHEMERAL_DATA_VALID:
			self.gpsLabel.SetLabel("GPS Ephemeral data valid until %s" % self.data.getQuickGPSExpiry())
		elif quickGPSValidity == self.data.EPHEMERAL_DATA_MISSING:
			self.gpsLabel.SetLabel("GPS Ephemeral data file not found")
		elif quickGPSValidity == self.data.EPHEMERAL_DATA_EXPIRED:
			self.gpsLabel.SetLabel("GPS Ephemeral data expired on %s" % self.data.getQuickGPSExpiry())
			self.gpsUpdateButton.Enable()
		else:
			self.gpsLabel.SetLabel("GPS Ephemeral status unknown")
		self.tomtomLocationLabel.SetLabel("%s" % self.data.getTomTomDir())


	def loadData(self):
		# Load All Routes in /route folder
		routeDir = os.path.join(self.data.getTomTomDir(), 'itn')		
		if os.path.isdir(routeDir):
			itnFiles = listFiles(routeDir, '.itn')
			self.importitnfiles(itnFiles)

	def changeTomTomDirGUI(self, event):
                chooser = wx.DirDialog(self, "TomTom Dir", self.data.getTomTomDir(), wx.DD_DIR_MUST_EXIST, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
                	self.setTomTomDir(chooser.GetPath())

	def setTomTomDir(self, dir):
		self.data.setTomTomDir(dir)
		self.loadData()
		self.updateGPSPanel()

        def edititn(self, event):
                selectedITNIndex = self.guiITNListBox.GetSelection()
                waypoint = self.routeIndex[selectedITNIndex]
                itnEdit = ITNEdit(self, -1, waypoint)
                self.routeIndex[selectedITNIndex] = itnEdit.GetRecord()
                selectedRoute = self.guiITNCatListBox.GetStringSelection()
                self.data.removeRoute(selectedRoute)
                self.data.addRoute(selectedRoute, self.routeIndex.values())
                self.updateITNGUI()

        def editpoi(self, event):
                selectedPOIIndex = self.guiPOIListBox.GetSelection()
                poiRow = self.poiIndex[selectedPOIIndex]
                poiEdit = POIEdit(self, -1, poiRow)
                self.poiIndex[selectedPOIIndex] = poiEdit.GetRecord()
                selectedPOICategory = self.guiPOICatListBox.GetStringSelection()
                self.data.removePOIs(selectedPOICategory)
                self.data.addPOIs(selectedPOICategory, self.poiIndex.values())
                self.updatePOIGUI()
                
        def setmapdirGUI(self, event):
                chooser = wx.DirDialog(self, "Map Dir", self.data.getTomTomDir(), wx.DD_DIR_MUST_EXIST, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
			self.setmapdir(chooser.GetPath())

        def setmapdir(self, dir):
		poiFiles = listFiles(dir, '.ov2')
		self.importov2files(poiFiles)	
                        
	destTypeName = {0 : 'Via', 1 : '', 2 : 'Arrive', 3 : 'Start', 4 : 'Start'}

	def updateITNGUI(self):
		self.guiITNListBox.Clear()
		selectedRoute = self.guiITNCatListBox.GetStringSelection()
		self.route = self.data.getRoute(selectedRoute)
		self.routeIndex = dict()
		for waypoint in self.route:
			self.routeIndex[self.guiITNListBox.Append("%s %s" % (self.destTypeName[waypoint[3]], waypoint[2]))]=waypoint
	
	def updateITNCatGUI(self):
		self.guiITNCatListBox.Clear()
		for routeName in self.data.routes():
			self.guiITNCatListBox.Append(routeName)

	def itnCatSelect(self, event):
		self.updateITNGUI()

        def updatePOIGUI(self):
                self.guiPOIListBox.Clear()
                selectedPOICategory = self.guiPOICatListBox.GetStringSelection()
                self.pois = self.data.getPOIs(selectedPOICategory)
                self.poiIndex = dict()
                for poiRow in self.pois:
                        self.poiIndex[self.guiPOIListBox.Append(poiRow[0])]=poiRow
                
        def updatePOICatGUI(self):
                #Remove all categories and re-add
                self.guiPOICatListBox.Clear()
                for poiCategory in self.data.categories():
                        self.guiPOICatListBox.Append(poiCategory)
                
        def poiCatSelect(self, event):
                self.updatePOIGUI()

        def about(self, event):
                dlg = wx.MessageDialog(self, "JimJim HOME\n"
                                        "Author: Barry John Williams\n"
                                        "Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence\n",
                              "About", wx.ID_OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

        #def exportov2files(self, event):
        #        self.SetStatusText("Saving to %s" % self.data.getTomTomDir())
        #        self.data.createFiles(self.data.getTomTomDir())

	def importitnfiles(self, files):
                for file in files:
                        self.SetStatusText("Loading from %s" % file)
                        route = libitn.readITN(file)
                        routename = os.path.basename(file)[:-4]
                        self.data.addRoute(routename,route)
                        self.SetStatusText("Read %s records" % len(route))
                self.updateITNCatGUI()

	def importitn(self, event):
                chooser = wx.FileDialog(self, "Open Route Files", self.data.getTomTomDir(), "", "Tomcat Itinary (*.itn)|*.itn", wx.FD_MULTIPLE, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
                	files = chooser.GetPaths()
                	self.importitnfiles(files)
		chooser.Destroy()

	def exportitn(self, event):
                chooser = wx.FileDialog(self, "Save Route File", self.data.getTomTomDir(), "", "Tomcat Itinary (*.ov2)|*.ov2", wx.FD_SAVE, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
                	f = chooser.GetPath()
                	route = self.data.getRoute(self.guiITNCatListBox.GetStringSelection())
                	libitn.writeITN(route,f)
                	self.SetStatusText("Saved %s" % f)
                chooser.Destroy()

        def importov2files(self, files):
                for file in files:
                        self.SetStatusText("Loading from %s" % file)
                        poiset = libov2.readOV2(file)
			if len(poiset) > 0:
                        	categoryname = os.path.basename(file)[:-4]
                        	self.data.addPOIs(categoryname,poiset)
                        	self.SetStatusText("Read %s records" % len(poiset))
                self.updatePOICatGUI()

	def mergeov2(self, event):
                chooser = wx.FileDialog(self, "Open POI Files", self.data.getTomTomDir(), "", "Tomcat Overlay (*.ov2)|*.ov2", wx.FD_MULTIPLE, wx.DefaultPosition)
                selectedPOICategory = self.guiPOICatListBox.GetStringSelection()
		if selectedPOICategory == '':
			self.SetStatusText("No POI Category Selected for Merge")
		else:
                	if chooser.ShowModal() == wx.ID_OK:
                		files = chooser.GetPaths()
                		for file in files:
                        		self.SetStatusText("Loading from %s" % file)
                        		poiset = libov2.readOV2(file)
                        		self.data.addPOIs(selectedPOICategory,poiset)
                        		self.SetStatusText("Read %s records" % len(poiset))
                	self.updatePOIGUI()
                	chooser.Destroy()

        def importov2(self, event):
                chooser = wx.FileDialog(self, "Open POI Files", self.data.getTomTomDir(), "", "Tomcat Overlay (*.ov2)|*.ov2", wx.FD_MULTIPLE, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
                	files = chooser.GetPaths()
                	self.importov2files(files)
                chooser.Destroy()
                
        def exportov2(self, event):
                chooser = wx.FileDialog(self, "Save POI File", self.data.getTomTomDir(), "", "Tomcat Overlay (*.ov2)|*.ov2", wx.FD_SAVE, wx.DefaultPosition)
                if chooser.ShowModal() == wx.ID_OK:
                	f = chooser.GetPath()
                	poiset = self.data.getCategory(self.guiPOICatListBox.GetStringSelection())
                	libov2.writeOV2(poiset,f)
                	self.SetStatusText("Saved %s" % f)
                chooser.Destroy()
                                
        def exit(self, event):
                self.Close(True)

if __name__ == '__main__':
        app = wx.App()
        poiFrame = POIFrame(None, -1, "JimJim HOME")
        if len(sys.argv) > 1:
                relpath = os.path.join(os.getcwd(),sys.argv[1])
                dir = os.path.realpath(relpath)
		poiFrame.setTomTomDir(dir)
        poiFrame.Show(True)
        app.MainLoop()
