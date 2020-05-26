#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Link and reference check tool to assist with asciidoctor publishing
#
# Syntax: adoc-link-check.py <path/to/adoc/files>
#
#
# AsciiDoc syntax expectations:
#
# [[link]] always start at begin of line and line contains nothing but link
# <<link,title>> is parsed wherever found, even in source code blocks.
#
# Warnings are issued when:
# - link is not found
# - link starts with number (invalid)

import os
import glob
import sys
import ntpath

def processAdoc(fpath, mode, scriptPath):
	try:
		adocDirPath, adocFName = ntpath.split(fpath)
		print("\nProcessing '{}' in '{}'".format(adocFName, adocDirPath))
		
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
				imagesdir = os.path.abspath(os.path.join(adocDirPath, imagesdir))
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
				
				# check for existing file
				if len(imagesdir) != 0:
					fullImagePath = os.path.join(imagesdir, imagefname)
				else:
					fullImagePath = os.path.join(adocDirPath, imagefname)
				if not os.path.exists(fullImagePath):
					raise RuntimeError("{}:{}:Image file {} ({}) not found".format(adocFName, i+1, imagefname, fullImagePath))

				# now we check for -print suffix 
				(basename,ext) = os.path.splitext(imagefname)
				posPrint = basename.rfind(PRINT_FILE_SUFFIX)
				# do we have a filename without 
				if posPrint == -1:
					htmlName = basename + ext
					pdfName = basename + PRINT_FILE_SUFFIX + ext
				else:
					htmlName = basename[:-len(PRINT_FILE_SUFFIX)] + ext
					pdfName = basename + ext
				
				# based on mode, determine target filename
				if mode == "html":
					targetFile = htmlName
				else:
					targetFile = pdfName
				# check if it exists
				if len(imagesdir) != 0:
					fullTargetPath = os.path.join(imagesdir, targetFile)
				else:
					fullTargetPath = os.path.join(adocDirPath, targetFile)
				if not os.path.exists(fullTargetPath):
					print("  WARNING: Target file {} not found, keeping original file name".format(targetFile))
					targetFile = imagefname
				# now replace filenames
				line = line[0:pos] + targetFile + line[pos2:]
					
				pos = line.find("image:", pos2)
			# while loop end
			
			# store (potentially) modified line object
			lines[i] = line
			
		# for loop end
		
		
		# finally dump out the file again
		fobj = open(fpath, 'w')
		fobj.writelines(lines)
		fobj.close()
		del fobj
		
		
	except IOError as e:
		print(str(e))
		raise RuntimeError("Error processing adoc file.")



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
	print("Processing '{}' in '{}' mode.".format(adocdir, mode))
	
	# process all adoc files
	for f in glob.glob(adocdir+"/*.adoc"):
		fullPath = os.path.abspath(f)
		processAdoc(fullPath, mode, scriptFilePath)
	
except RuntimeError as e:
	print(str(e))
	exit(1)

exit(0)
