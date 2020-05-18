#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Image exchange tool to assist with asciidoctor publishing
#
# Syntax: adoc-image-prep.py <html|pdf> <path/to/adoc/files>

import os
import glob
import sys
import ntpath

def processAdoc(fpath, mode, scriptPath):
	try:
		adocFilePath, adocFName = ntpath.split(fpath)
		print("\nProcessing '{}' in '{}'".format(adocFName, adocFilePath))
		
		# read the file
		fobj = open(fpath, 'r')
		lines = fobj.readlines()
		fobj.close
		del fobj
		
		imagesdir = ""
		# now process line by line, search for :imagesdir: property
		for i in range(len(lines)):
			line = lines[i]
			pos = line.find(":imagesdir:")
			if pos != -1:
				imagesdir = line[11:].strip()
				imagesdir = os.path.abspath(os.path.join(adocFilePath, imagesdir))
				print ("  Images dir = '{}'".format(imagesdir))
				continue
			# search for image: or image:: in text
			pos = line.find("image:")
			while (pos != -1):
				if len(line) > pos+2:
					if line[pos+6] == ':':
						pos = pos + 7
					else:
						pos = pos + 6
				# search for first delimiter, either [ or ' '
				pos_braket = line.find("[", pos)
				pos_space = line.find(" ", pos)
				pos2 = pos_braket
				if pos_space != -1:
					if pos2 != -1:
						if pos_space < pos_braket:
							pos2 = pos_space
					else:
						pos2 = pos_space
				# pos2 now either holds the position of the first space, first '[' or -1 (end of line)
				imagefname = line[pos:pos2].strip()
				print("  Image ref = {}".format(imagefname))
				# image tag is delimited by [ or space or tab
				#print("'{}'".format(line[pos:pos2]))
				pos = line.find("image:", pos2)
				
	except IOError as e:
		print(str(e))
		raise RuntimeError("Error processing adoc file.")



# --- Main program start ---

try:
	# get current working directory, in case we need to resolve relative paths
	scriptFilePath = os.getcwd()

	# check command line
	if len(sys.argv) < 3:
		if len(sys.argv) == 2 and sys.argv[1] == "--help":
			print("Syntax: adoc-image-prep.py <html|pdf> <path/to/adoc/files>")
			exit(0)
	
		raise RuntimeError("Invalid command line, expected three arguments.")

	mode = sys.argv[1]
	adocdir = sys.argv[2]
	print("Processing '{}' in '{}' mode.".format(adocdir, mode))
	
	# process all adoc files
	for f in glob.glob(adocdir+"/*.adoc"):
		fullPath = os.path.abspath(f)
		processAdoc(fullPath, mode, scriptFilePath)
	
except RuntimeError as e:
	print(str(e))
	exit(1)

exit(0)
