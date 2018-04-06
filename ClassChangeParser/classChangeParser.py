import sys
import os
import shutil
import re

toc = '[toc]'
separator = '[/toggler][/div][/toggler]'
directory = 'output'
tail = '[/toggler][/div]'
baseHeader = '[h2][color={1}]{0} Spell Changes[/color][/h2][div class="patch-diff patch-diff-group-{2} patch-diff-class patch-diff-class-{3}"]'
nameRe = re.compile('(name=").*?(")')
colorRe = re.compile('(class=").*?(")')

#[h2][color=c6]Death Knight Spell Changes[/color]
#[toggler name="Death Knight" size=2 class="c6" icon="class_deathknight" closed=false]

#[h2][color={1}]{0} Spell Changes[/color]

# Verifies if an argument was provided
if len(sys.argv) > 1:
	providedFile = sys.argv[1]

	# Verifies if it is a valid file name
	# TODO: alert if it isn't valid
	if os.path.exists(providedFile):
		contents = None

		# Extract contents from file
		with open(providedFile, 'r') as f:
			contents = f.read()

	    # Check if output directory exists, if not, creates it
		if not os.path.exists(directory):
			os.makedirs(directory)

		# Changes to the output directory and removes all previous files form it
		os.chdir(directory)

		for the_file in os.listdir('.'):
		    file_path = os.path.join('.', the_file)
		    try:
		        if os.path.isfile(file_path):
		            os.unlink(file_path)
		        elif os.path.isdir(file_path): shutil.rmtree(file_path)
		    except Exception as e:
		        print(e)

	    # Splits the content by class and prints each on its file
		for clss in contents.split(toc)[1].split(separator):

			content = clss.strip()
			firstLine = clss.strip().split('\n')[0]
			if nameRe.search(firstLine) is not None:

				clsName = nameRe.search(firstLine).group(0)[6:-1]
				color = colorRe.search(firstLine).group(0)[7:-1]
				header = baseHeader.format(clsName, color, '-'.join( clsName.split(' ') ).lower(), color[1:] )

				with open('{0}.txt'.format(clsName), 'w') as f:
					f.seek(0)
					f.write(header)
					f.write('\n'.join(content.split('\n')[1:]))
					f.write(tail)
					f.truncate()
