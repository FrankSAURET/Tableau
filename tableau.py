#!/usr/bin/env python 
# coding: utf-8 
 
# toutes les chaines sont en unicode (même les docstrings)
from __future__ import unicode_literals

"""
tableau.py
Création de tableau simple pour Inkscape

Codé par Frank SAURET - http://www.electropol.fr - 

License : Public Domain

"""

import inkex

__version__ = '2020.2'
# Version validée pour Inkscape 1.02

inkex.localization.localize()

class Tableau(inkex.GenerateExtension):
	def add_arguments(self, pars):
		#Récupération des paramêtres
		pars.add_argument("--rows", type=int, dest="NbLigne", default=2, help="Nombre de lignes")
		pars.add_argument("--cols", type=int, dest="NbColonne", default=3, help="Nombre de colonnes")
		pars.add_argument("--units", type=str, dest="Unitee", default="mm", help="Unitée pour la cellule")
		pars.add_argument("--width", type=float, dest="CelL", default=10.0, help="Largeur de la cellule")
		pars.add_argument("--height", type=float, dest="CelH", default=20.0, help="Hauteur de la cellule")
		pars.add_argument("--weight", type=float, dest="ETrait", default=0.1, help="Epaisseur des traits")
		pars.add_argument("--color", type=inkex.Color, dest="Couleur", default=inkex.Color(0), help="Couleur des traits")
		pars.add_argument("--round", type=float, dest="Arrondi", default=10.0, help="Rayon de l'arrondi")
		pars.add_argument("--active-tab", type=str, dest="active_tab", default="options", help="Active tab.")

	def generate(self):
		#Récupération des dimensions d'une cellule selon l'unitée
		HauteurCellule=self.svg.unittouu( str(self.options.CelH)  + self.options.Unitee )
		LargeurCellule=self.svg.unittouu( str(self.options.CelL)  + self.options.Unitee )
		EpaisseurTrait=self.svg.unittouu( str(self.options.ETrait)  + self.options.Unitee )
		
		rf=self.svg.unittouu(str(self.options.Arrondi)+ self.options.Unitee )
		r=str(rf)
		#Les éléments de dessin
		Ahd=' a '+r+','+r+' 0 0 1 '+r+','+r
		Abd=' a '+r+','+r+' 0 0 1 -'+r+','+r
		Abg=' a '+r+','+r+' 0 0 1 -'+r+',-'+r
		Ahg=' a '+r+','+r+' 0 0 1 '+r+',-'+r
		BordGauche=Ahg+Abg
		BordDroit=' m '+r+',-'+r+Abd+Ahd
		Croisillon=Ahd+Ahg+Abg+Abd
		SegmentH=' h '+ str(self.svg.unittouu( str(self.options.CelL-2*self.options.Arrondi)  + self.options.Unitee ))
		SegmentV=' v '+ str(self.svg.unittouu( str(self.options.CelH-2*self.options.Arrondi)  + self.options.Unitee ))
		SegmentHNeg=' h -'+ str(self.svg.unittouu( str(self.options.CelL-2*self.options.Arrondi)  + self.options.Unitee ))
		DeplacementV=str(self.svg.unittouu( str(self.options.CelH-2*self.options.Arrondi)  + self.options.Unitee ))

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
		style = inkex.Style({	
				'fill'          : 'none',
				'stroke'        : self.options.Couleur,
				'stroke-width'  : EpaisseurTrait
				})

		return inkex.PathElement(d=tableau_path, style=str(style))

if __name__ == '__main__':
    Tableau().run()