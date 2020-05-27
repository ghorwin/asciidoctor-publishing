#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of asciidoctor-publishing git repo.
# Written by Andreas Nicolai <andreas.nicolai -at- gmx[dot]net>.
#
# Link and reference check tool to assist with asciidoctor publishing
#
# Syntax: adoc-link-check.py <path/to/adoc/files>
#
#
# AsciiDoc syntax expectations:
#
# - [[link]] always start at begin of line and line contains nothing but link
# - [[link]] may be followed in next line by header section, i.e. # on start of next line, 
#            header title is used for annotating the label
# - [[link]] may be followed a title .xxx in next line, title is used for annotating the label 
# - <<link,title>> and <<link>> is parsed wherever found, even in source code blocks.
#
# Warnings are issued when:
# - link is not found
# - link starts with number (invalid)

import os
import glob
import sys
import ntpath

from print_funcs import *

def haveDuplicateLinkLabel(label, links):
	"""Checks if given label exists already in list of link labels.
	
	**Arguments**
	
	*label*
	  the label to search for
	  
	*links*
	  list with link labels collected so far, 
	  list contains tuples of (label, filename, line nr., description, is_duplicate)

	**Returns**
	
	True, if such a label exists already in the list, False if not.
	"""
	
	for l in links:
		if l[0] == label:
			printError("    Duplicate label '{}' found at {}:{}".format(label, l[1], l[2]))
			return True
	
	return False



def scanForLinkLabels(fpath, links):
	"""Processes asciidoctor input file:
	
	**Arguments**
	
	*fpath*
	  full file path to Ascii-Doctor input file
	  
	*links*
	  list with link labels collected so far (will be modified in function),
	  list contains tuples of (label, filename, line nr., description, is_duplicate)
	"""
	
	try:
		adocDirPath, adocFName = ntpath.split(fpath)
		#print("\n  {}".format(adocFName))
		
		# read the file
		fobj = open(fpath, 'r')
		lines = fobj.readlines()
		fobj.close
		del fobj
		
		# now process line by line, search for [[xxx]] pattern
		for i in range(len(lines)):
			line = lines[i]
			pos = line.find("[[")
			# does line start with [[ ?
			if pos == 0: 
				pos2 = line.find("]]",3)
				if pos2 != -1:
					# found new link label
					link_label = line[2:pos2].strip()
					if len(link_label) == 0:
						printError("    empty label at {}:{}".format(adocFName, i))
						continue
					desc = ""
					if i < len(lines):
						nextLine = lines[i+1]
						if len(nextLine) != 0:
							# check if following line contains a caption
							if nextLine[0] == "#":
								desc = nextLine.strip()
							# check if following line contains a caption
							elif nextLine[0] == ".":
								desc = nextLine[1:].strip()
							elif nextLine.find("image::"):
								desc = nextLine[8:].strip()
					# check if such label exists already somewhere
					if not haveDuplicateLinkLabel(link_label, links):
						links.append( (link_label, adocFName, i, desc, False) )
					else:
						links.append( (link_label, adocFName, i, desc, True) )
						print("    and {}:{}".format(adocFName, i))
		
	except IOError as e:
		print(str(e))
		raise RuntimeError("Error processing adoc file.")


def checkReferences(fpath, links):
	"""Processes asciidoctor input file:
	
	**Arguments**
	
	*fpath*
	  full file path to Ascii-Doctor input file
	  
	*links*
	  list with link labels collected so far
	"""
	pass

# --- Main program start ---

try:
	# get current working directory, in case we need to resolve relative paths
	scriptFilePath = os.getcwd()

	# check command line
	if len(sys.argv) == 2 and sys.argv[1] == "--help":
		print("Syntax: adoc-link-check.py <path/to/adoc/files>")
		exit(0)

	if len(sys.argv) < 2:
		raise RuntimeError("Invalid command line, expected path argument.")

	adocdir = sys.argv[1]
	#print("Processing '{}'.".format(adocdir))
	
	# process all adoc files - first pass, scan for [[xxx]] link labels
	links = []
	for f in glob.glob(adocdir+"/*.adoc"):
		fullPath = os.path.abspath(f)
		scanForLinkLabels(fullPath, links)
	
	# sort labels by link label
	links = sorted(links, key=lambda tup: tup[0])
	# dump out a list of all labels
	for l in links:
		loc = "{}:{}".format(l[1], l[2])
		# either a duplicate or bad label name - print as error
		if l[4] or l[0][0].isdigit():
			printError("{:<20s} {:<30s} '{}'".format(l[0], loc, l[3]) )
		else:
			print("{:<20s} {:<30s} '{}'".format(l[0], loc, l[3]) )
	
	# process all adoc files - second pass, scan for <<xxx>> references and print errors if encountered
	for f in glob.glob(adocdir+"/*.adoc"):
		fullPath = os.path.abspath(f)
		checkReferences(fullPath, links)
	
except RuntimeError as e:
	print(str(e))
	exit(1)

exit(0)
