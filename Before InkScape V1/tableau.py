#!/usr/bin/env python 
# coding: utf-8 
 
# toutes les chaines sont en unicode (même les docstrings)
from __future__ import unicode_literals

"""
tableau.py
Création de tableau simple pour Inkscape

Codé par Frank SAURET - http://www.electropol.fr - 

License : CC BY-NC-SA 3.0 FR
Attribution + Pas d’Utilisation Commerciale + Partage dans les mêmes conditions (BY NC SA): 
Le titulaire des droits autorise l’exploitation de l’œuvre originale à des fins non commerciales, 
ainsi que la création d’œuvres dérivées, à condition qu’elles soient distribuées sous une licence 
identique à celle qui régit l’œuvre originale.
"""

import inkex, simplestyle

__version__ = '1.0'

inkex.localize()

class Tableau(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)# Initialisation de la super classe

		#Récupération des paramêtres
		self.OptionParser.add_option(
			"", "--rows", 
			action="store", type="int",
			dest="NbLigne", default=2,
			help="Nombre de lignes")   
		self.OptionParser.add_option(
			"", "--cols", 
			action="store", type="int",
			dest="NbColonne", default=3,
			help="Nombre de colonnes")  
		self.OptionParser.add_option(
			"", "--units", 
			action="store", type="string",
			dest="Unitee", default='mm',
			help="Unitée pour la cellule")  
		self.OptionParser.add_option(	
			"", "--width", 
			action="store", type="float",
			dest="CelL", default=10,
			help="Largeur de la cellule")  
		self.OptionParser.add_option(
			"", "--height", 
			action="store", type="float",
			dest="CelH", default=20,
			help="Hauteur de la cellule")  
		self.OptionParser.add_option(
			"", "--weight", 
			action="store", type="float",
			dest="ETrait", default=0.1,
			help="Epaisseur des traits")  
		self.OptionParser.add_option(
			"", "--color", 
			action="store", type="string",
			dest="Couleur", default=0,
			help="Couleur des traits")
		self.OptionParser.add_option(	
			"", "--round", 
			action="store", type="float",
			dest="Arrondi", default=10,
			help="Rayon de l'arrondi")  			
		self.OptionParser.add_option(
			"", "--active-tab",
			action="store", type="string",
			dest="active_tab", default='options', 
			help="Active tab.")								 

	def getColorString(self, longColor, verbose=False):
		""" Convert the long into a #RRGGBB color value
		and transparency (0 to 1)
		- verbose=true pops up value for us in defaults
		"""
		if verbose: inkex.debug("%s ="%(longColor))
		longColor = long(longColor)
		if longColor <0: longColor = long(longColor) & 0xFFFFFFFF
		Transparency=format((longColor%256)/256.0,'.8f')
		hexColor = '#' + format(longColor/256, '06X')
		if verbose: inkex.debug("  %s for color default value"%(hexColor))
		return [hexColor, Transparency]
		
	def effect(self):
		Couleur = self.getColorString(self.options.Couleur)[0]
		Transparence= self.getColorString(self.options.Couleur)[1]
		#Récupération des dimensions d'une cellule selon l'unitée
		HauteurCellule=self.unittouu( str(self.options.CelH)  + self.options.Unitee )
		LargeurCellule=self.unittouu( str(self.options.CelL)  + self.options.Unitee )
		EpaisseurTrait=self.unittouu( str(self.options.ETrait)  + self.options.Unitee )
		
		rf=self.unittouu(str(self.options.Arrondi)+ self.options.Unitee )
		r=str(rf)
		#Les éléments de dessin
		Ahd=' a '+r+','+r+' 0 0 1 '+r+','+r
		Abd=' a '+r+','+r+' 0 0 1 -'+r+','+r
		Abg=' a '+r+','+r+' 0 0 1 -'+r+',-'+r
		Ahg=' a '+r+','+r+' 0 0 1 '+r+',-'+r
		BordGauche=Ahg+Abg
		BordDroit=' m '+r+',-'+r+Abd+Ahd
		Croisillon=Ahd+Ahg+Abg+Abd
		SegmentH=' h '+ str(self.unittouu( str(self.options.CelL-2*self.options.Arrondi)  + self.options.Unitee ))
		SegmentV=' v '+ str(self.unittouu( str(self.options.CelH-2*self.options.Arrondi)  + self.options.Unitee ))
		SegmentHNeg=' h -'+ str(self.unittouu( str(self.options.CelL-2*self.options.Arrondi)  + self.options.Unitee ))
		DeplacementV=str(self.unittouu( str(self.options.CelH-2*self.options.Arrondi)  + self.options.Unitee ))
					
		#Tracé du tableau avec rattrapage de l'épaisseur des traits et arrondis
		## Positionnement du début du tableau
		y=str(rf)
		x=str(0)
		tableau_path=' M '+x+','+y
		
		##Tracé de la première ligne (pour optimiser le déplacement du laser)
		for i in range (0,self.options.NbColonne):
			tableau_path=tableau_path+Ahg+SegmentH+Ahd
		
		## Tracé des lignes médianes (pour optimiser le déplacement du laser)
		DecalageD=' m '+r+','+r
		DecalageM=' m '+str(2*rf)+',0'
		for i in range (1,self.options.NbLigne):
			y=str(rf+i*HauteurCellule)
			#Première cellule
			tableau_path=tableau_path+'M 0,'+y+ BordGauche+DecalageD+SegmentH
			#Cellules suivantes
			for j in range (0,self.options.NbColonne-1):
				x=str(j*LargeurCellule)
				tableau_path=tableau_path+Croisillon+DecalageM+SegmentH
			#Dernière cellule	
			tableau_path=tableau_path+BordDroit
		
		##Tracé de la dernière ligne (dans l'autre sens pour optimiser le déplacement du laser)
		tableau_path=tableau_path+'m 0,'+DeplacementV
		for i in range (0,self.options.NbColonne):
			tableau_path=tableau_path+Abd+SegmentHNeg+Abg
		
		#Tracé des colonnes
		for i in range (0,self.options.NbColonne+1):
			x=str(i*LargeurCellule)
			for j in range (0,self.options.NbLigne):
				y=str(j*HauteurCellule+rf)
				tableau_path=tableau_path+' M '+x+','+y+SegmentV			
		
		#Construction puis écriture du chemin
		style = {	
				'fill'          : 'none',
				'stroke'        : Couleur,
				'stroke-width'  : EpaisseurTrait,
				'stroke-opacity': Transparence
				}
		tableau_id = self.uniqueId('tableau')	
		tableau_parent = self.current_layer
		tableau_attributs = {
							'd': tableau_path, 
							'style': simplestyle.formatStyle(style),
							'id':tableau_id
							}
		inkex.etree.SubElement(tableau_parent, inkex.addNS('path','svg'), tableau_attributs)

if __name__ == '__main__':   
	e = Tableau()
	e.affect()
