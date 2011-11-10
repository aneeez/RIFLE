#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    RIFLE v1.0 - A Kickass tool to convert your auidio and video files
#    Copyright (C) 2011  
#    Author - Nakul Ezhuthupally <nakule@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>


try:
	
	
	import gtk.glade, os
	
	import subprocess, time

except ImportError:
	

	print "Some of the modules required for RIFLE is not available"

	print "Make sure you have these modules available in your system\n"

	print "-> gtk.glade\n-> os\n-> subprocess\n-> time"

	print "\nQuitting....."

	exit(1)




class MainLoop:
	
	
	wtree=None
	
	liststore=None
	
	chooseavfile=None
	
	liststoredummy=[]
	
	isrunning=False
	
	fp=None
	
	extensions=["Video Formats","avi","flv","mpg","mkv","mov","mp4","ogg","rm","swf","vob","wmv","Audio Formats","aac","ac3","aiff","mp3","ogg","wav","wma"]
	



	# # # # # # # # # # # # # # # # # # # # # # # # #
	# Connecting Python program with the GLADE file #
	# # # # # # # # # # # # # # # # # # # # # # # # #
	
	def __init__(self):
		
	
		self.wtree=gtk.glade.XML("/usr/share/RIFLE/gtree.glade")
		
	
		if self.wtree != None:
			
			print "\n\n\n\n\nConnect to the Glade File..............[O.K]"
		
	
		dic = {
		
					"on_windowMain_destroy" : self.safequit,
					
					"on_buttonAdd_clicked" : self.clickedadd,
					
					"on_buttonClear_clicked" : self.clickedclear,
										
					"on_buttonNoFFok_clicked" : self.safequit,
					
					"on_windowNoFF_destroy" : self.safequit,
					
					"on_buttonConvert_clicked" : self.clickedconvert,
					
					"on_buttonQuit_clicked" : self.safequit,
					
					"on_buttonAbout_clicked" : self.launchabout,
					
					"on_windowErrReport_delete_event" : self.dontdelete,
										
					"on_buttonErrClose_clicked" : self.clickederrclose,
					
					"on_buttonSkip_clicked" : self.skipconversion,
					
					"on_buttonSuccessOK_clicked" : self.hidesuccess,
					
					"on_buttonConfirmQuit_clicked" : self.killandquit,
					
					"on_buttonConfirmContinue_clicked" : self.hideconfirm,
					
					"on_windowMain_delete_event" : self.dontdeleteMain,
					
					"on_windowConfirmQuit_delete_event" : self.dontdelete,
					
					"on_windowSuccess_delete_event" : self.dontdelete,
					
					"on_buttonAboutClose_clicked" : self.closeabout,
					
					"on_windowAbout_delete_event" : self.dontdelete,
		}
		
		self.wtree.signal_autoconnect(dic)
		
		self.pre_initialization()
		
		gtk.main()
		
		


	# # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#   Check and set the environment for the pgm to run  #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # #
		
	def pre_initialization(self):
		
		
		# Build the Treeview and File Browser for later use
		
		self.buildtreeview()
		
		self.createfilechooser()
		
		
		# Set 'Video Formats' as the active item in combo box
		
		self.wtree.get_widget("comboboxExt").set_active(0)
		
		
		# Make the convert and skip button insensitive
		
		self.wtree.get_widget("buttonConvert").set_sensitive(False)
		
		self.wtree.get_widget("buttonSkip").set_sensitive(False)
		
		
		# Set the Title for All Windows
		
		self.wtree.get_widget("windowMain").set_title("RIFLE - Convert your Audio and Video Files")
		
		self.wtree.get_widget("windowNoFF").set_title("RIFLE - No FFMPEG... !!!")
		
		self.wtree.get_widget("windowErrReport").set_title("RIFLE - Oops...")
		
		self.wtree.get_widget("windowSuccess").set_title("RIFLE - Yippee...")
		
		self.wtree.get_widget("windowConfirmQuit").set_title("RIFLE - Quit ?? Are you Sure ??")
		
		self.wtree.get_widget("windowAbout").set_title("About RIFLE")
		
		print "Set Titles for all windows..............[O.K]"
		
		
		# Set the width of MainWindow to 680px and make it visible
		
		self.wtree.get_widget("windowMain").set_size_request(680,-1)
		
		self.wtree.get_widget("windowMain").set_visible(True)
		
		
		# Make all windows non-resizable ; no maximize button
		
		self.wtree.get_widget("windowMain").set_resizable(False)
		
		self.wtree.get_widget("windowNoFF").set_resizable(False)
		
		self.wtree.get_widget("windowSuccess").set_resizable(False)
		
		self.wtree.get_widget("windowErrReport").set_resizable(False)
		
		self.wtree.get_widget("windowConfirmQuit").set_resizable(False)
		
		self.wtree.get_widget("windowAbout").set_resizable(False)
		
		print "Set all windows to non-resizable..............[O.K]"
		
		
		# Set Logo for all Windows
		
		self.wtree.get_widget("windowMain").set_icon_name("RIFLE")
		
		self.wtree.get_widget("windowNoFF").set_icon_name("RIFLE")
		
		self.wtree.get_widget("windowErrReport").set_icon_name("RIFLE")
		
		self.wtree.get_widget("windowSuccess").set_icon_name("RIFLE")
		
		self.wtree.get_widget("windowConfirmQuit").set_icon_name("RIFLE")
		
		self.wtree.get_widget("windowAbout").set_icon_name("RIFLE")
		
		print "Set logo for all windows................[O.K]"
		
		
		# Check if ffmpeg is installed in the system ; else, raise error
		
		self.check_if_ffmpeg_is_available()
		
	
	
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#   Check to see if FFmpeg is installed in the host system  #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	
	def check_if_ffmpeg_is_available(self):
		
	
		tmp="which ffmpeg"
		
		fp=subprocess.Popen(tmp,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		
		chk=False
		
	
		for x in fp.stdout:
			
			chk=True
			
	
		if (not chk):
			
			print "FFmpeg is not installed in your System"
			
			self.wtree.get_widget("windowMain").hide()
			
			self.wtree.get_widget("windowNoFF").show()
		
	
		else:
			
			print "Checking for installed FFmpeg in the s/m.............[O.K]"
		
		

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Build the treeview that will display the filenames to be processed  #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		
	def buildtreeview(self):
		
	
		treeview=self.wtree.get_widget("treeview")
		
		self.liststore=gtk.ListStore(str)
		
		treeview.set_model(self.liststore)
		
		
		column1=gtk.TreeViewColumn("File Name")
		
		column1.set_spacing(30)
		
		treeview.append_column(column1)
		
		cell=gtk.CellRendererText()

		cell.set_padding(8,8)
		
		column1.pack_start(cell, True)
		
		column1.add_attribute(cell, "text", 0)		
		
		print "Building Treeview...........[O.K]"
		



	# # # # # # # # # # # # # # # # # # # # # # # # # #
	# Create File Browser with required file filters  #
	# # # # # # # # # # # # # # # # # # # # # # # # #	
	
	def createfilechooser(self):
		
	
		self.chooseavfile=gtk.FileChooserDialog("Open AV Files", None, gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_ADD,gtk.RESPONSE_OK))
		
		self.chooseavfile.set_default_response(gtk.RESPONSE_OK)
		
		self.chooseavfile.set_select_multiple(True)
		
		filtr=gtk.FileFilter()
		
		filtr.set_name("Audio/Video")
		
		# Adding filters for video formats
		
		filtr.add_pattern("*.avi")
		filtr.add_pattern("*.AVI")
		
		filtr.add_pattern("*.3gp")
		filtr.add_pattern("*.3GP")
		
		filtr.add_pattern("*.MP4")
		filtr.add_pattern("*.mp4")
		
		filtr.add_pattern("*.MKV")
		filtr.add_pattern("*.mkv")
		
		filtr.add_pattern("*.ogg")
		filtr.add_pattern("*.OGG")
		
		filtr.add_pattern("*.MPG")
		filtr.add_pattern("*.mpg")
		
		filtr.add_pattern("*.MPEG")
		filtr.add_pattern("*.mpeg")
		
		filtr.add_pattern("*.flv")
		filtr.add_pattern("*.FLV")
		
		filtr.add_pattern("*.mov")
		filtr.add_pattern("*.MOV")
		
		filtr.add_pattern("*.vob")
		filtr.add_pattern("*.VOB")
		
		filtr.add_pattern("*.wmv")
		filtr.add_pattern("*.WMV")
		
		filtr.add_pattern("*.rmvb")
		filtr.add_pattern("*.RMVB")
		
		filtr.add_pattern("*.rm")
		filtr.add_pattern("*.RM")
		
		filtr.add_pattern("*.swf")
		filtr.add_pattern("*.SWF")
		
		
		# Adding filters for Audio Formats
		
		filtr.add_pattern("*.mp3")
		filtr.add_pattern("*.MP3")
		
		filtr.add_pattern("*.aac")
		filtr.add_pattern("*.AAC")
		
		filtr.add_pattern("*.ac3")
		filtr.add_pattern("*.AC3")
		
		filtr.add_pattern("*.aiff")
		filtr.add_pattern("*.AIFF")
		
		filtr.add_pattern("*.wav")
		filtr.add_pattern("*.WAV")
		
		filtr.add_pattern("*.wma")
		filtr.add_pattern("*.WMA")		
				
		self.chooseavfile.add_filter(filtr)

		print "Creating File Browser.........[O.K]"
		
		print "Setting Audio/Video Filters for i/p files............[O.K]"


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Run the filebrowser and add the selected files to the treeview  #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		
	def clickedadd(self,widget):
		
	
		response=self.chooseavfile.run()
		
		print "Running File Browser..........[O.K]"
		
	
		if response == gtk.RESPONSE_OK:
			
			self.wtree.get_widget("buttonConvert").set_sensitive(True)
			
			filenames = self.chooseavfile.get_filenames()
			
			print "The Following Files will be added to the Treeview\n"
			
	
			for x in filenames:
				
				print x
				
				self.liststore.append([x])
				
				self.liststoredummy.append(x)
				
	
			print "\nAdding selected files to the treeview........[O.K]"
							
	
		elif response == gtk.RESPONSE_CANCEL:
			
			print "No File has been Selected"
			
	
		self.chooseavfile.hide()



	
	# # # # # # # # # # # # # # # # # # # # # #
	# Clear the Treeview and the backend list #
	# # # # # # # # # # # # # # # # # # # # # #	
		
	def clickedclear(self,widget):
		
	
		self.liststore.clear()
		
		self.wtree.get_widget("buttonConvert").set_sensitive(False)
		
		l=len(self.liststoredummy)
		
		print "Clearing treestore of the following files\n"
		
	
		for x in range(0,l):
			
			y=self.liststoredummy.pop()
			
			print y
		
	
		self.liststoredummy=[]
		
		print "\nClearing treestore.......[O.K]"


				
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Get the duration of the i/p file so as to calculate progress  #
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	
	def get_duration_of_ipfile(self,ipfile):
				
	
		cmd=["ffmpeg","-i",ipfile]
		
		fp=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
		
		fp.wait()
		
		duration=-1
		
	
		for x in fp.stderr:
		
			i=x.find("Duration:")
		
	
			if i!=-1:
		
				j=x.find(",")
		
				y=x[i+9:j]
		
				x=y.split(":")
				
				print x
		
				duration=(int(x[0])*3600)+(int(x[1])*60)+(float(x[2]))
				
	
		if duration == -1:
			
			print "The Duration of the i/p file could not be calculated => No Progress Bar"
			
	
		else:
			
			print "Duration of the i/p file in seconds => ",duration
		
		return duration	

		
		
		
	# # # # # # # # # # # # # # # # # # # # # # #
	# Things to take care of before conversion  #
	# # # # # # # # # # # # # # # # # # # # # # #
	
	def pre_conversion(self):
		
		self.isrunning=True
			
		self.wtree.get_widget("progressbarSingle").set_fraction(0)
		
		self.wtree.get_widget("progressbarAll").set_fraction(0)
					
		self.wtree.get_widget("hbox4").set_sensitive(False)
		
		self.wtree.get_widget("buttonSkip").set_sensitive(True)
		
		self.wtree.get_widget("hbox5").set_sensitive(False)
		
		self.wtree.get_widget("buttonConvert").set_sensitive(False)
		
		self.wtree.get_widget("windowProgress").set_sensitive(True)
					
		self.wtree.get_widget("windowProgress").show()
		
		print "setting the pre-requisites for conversion......[O.K]"



		
	# # # # # # # # # # # # # # # # # # # # # #
	# Things to take care of after conversion #
	# # # # # # # # # # # # # # # # # # # # # #
		
	def post_conversion(self):
		
		self.isrunning=False
		
		self.wtree.get_widget("progressbarSingle").set_fraction(1)
		
		self.wtree.get_widget("progressbarAll").set_fraction(1)
			
		self.wtree.get_widget("hbox4").set_sensitive(True)
		
		self.wtree.get_widget("hbox5").set_sensitive(True)
		
		self.wtree.get_widget("buttonConvert").set_sensitive(True)
		
		self.wtree.get_widget("windowProgress").set_sensitive(False)
		
		self.wtree.get_widget("buttonSkip").set_sensitive(False)
		
		time.sleep(0.9)
		
		self.wtree.get_widget("windowProgress").hide()
		
		print "Running the post-conversion cleanup........[O.K]"
	



	# # # # # # # # # # # # # # # # #
	# The Actual Conversion Process #
	# # # # # # # # # # # # # # # # #
				
	def clickedconvert(self,widget):
		
		
		# Get the Active selection in the combobox
		
		opext=self.wtree.get_widget("comboboxExt").get_active()
								
	
		# If 'Video Format' or 'Audio Format' is selected; Return
		
		if opext==0 or opext==12:
			
			print "Select a Valid File Format"
			
			return
			
			
		self.pre_conversion()
		
		
		errorfilenames=[]
		
		hasbeenerrors=False
		
		n=len(self.liststoredummy)
		
		no=0
		
		
		# Process each i/p file in the Treeview
		
		for ipfile in self.liststoredummy:
			
			
			# Hack to unzombie the GUI
			
			while gtk.events_pending():
			
				gtk.main_iteration()
		
			
			print "Currently Processing ===> ",ipfile
			
			
			filename=os.path.split(ipfile)[1]
			
			filename=os.path.splitext(filename)[0]
			
			
			# Get the Destination Directory
			
			oppath=self.wtree.get_widget("fileDestination").get_filename()
			
			opfile=os.path.join(oppath,filename) + "." + self.extensions[opext]
			
			i=1
			
			
			while os.path.isfile(opfile):

 				print "File already exists, so changing target filename"

				opfile=os.path.join(oppath,filename) + '(' + str(i) + ').' + self.extensions[opext]

				print "New Target o/p file ==> ",opfile

				i+=1
				
			
			duration=self.get_duration_of_ipfile(ipfile)
			
			cmd=["ffmpeg", "-i", ipfile, "-y", "-xerror"]
			
			
			if self.wtree.get_widget("checkbuttonQuality").get_active():
				
				cmd.append("-sameq")
				
				print "Retain the quality of the i/p file"
				
				
			else:
				
				print "Do not retain i/p quality"
				
			
			cmd.append(opfile)
			
			print "\n\nIssuing the command => ", cmd, "\n\n"
						
			self.fp=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0,universal_newlines=True)
			
			
			# Run while the conversion is in progress
			
			while self.fp.poll() == None:
				
				
				# Hack to unzombie the GUI
				
				while gtk.events_pending():
			
					gtk.main_iteration()
					
					
				line=self.fp.stderr.readline()


				while line and self.fp.poll()==None:
					
					
					# Hack to unzombie the GUI
					
					while gtk.events_pending():
			
						gtk.main_iteration()
					

					print line

			
					try:
						
						x=line.find("time=")

			
						while (line.find('time=') == -1) and self.fp.poll()==None:

							line=self.fp.stderr.readline()
							
							x=line.find("time=")
						
			
						y=line.find(".",x)

						dur=int(line[(x+5):y])
						
						print duration,"<- Total Duration\nCurrent Duration ->",dur

						
						try:
						
							perc=(float(dur)/duration)
							
							totalprogress=float(no)/n
													
							totalprogress=totalprogress+(perc/n)
						
						
						except ZeroDivisionError:
							
							perc=1
							
							totalprogress=float(no)/n
						
					
						self.wtree.get_widget("progressbarSingle").set_fraction(perc)
						
						text="Converting file " + str(no+1) + " of " + str(n) + " (" + str(int(perc*100)) + "%)"
						
						print "\n\n",text
			
						self.wtree.get_widget("progressbarSingle").set_text(text)
			
						text="Total Progress (" + str(int(totalprogress*100)) + "%)"
						
						print text
						
						self.wtree.get_widget("progressbarAll").set_text(text)
						
						self.wtree.get_widget("progressbarAll").set_fraction(totalprogress)

						line=self.fp.stderr.readline()

					
					except ValueError:

						print "Finished Conversion....."
				
				
				time.sleep(0.1)
			
			
			if self.fp.returncode:
				
				errorfilenames.append(os.path.split(ipfile)[1])
				
				hasbeenerrors=True
			
			
			no=no+1
			
					
		if hasbeenerrors:
			
			print "There has been errors in the conversion\n\n"
			
			errmsg="The following file(s) were not converted\n\n"
			
			
			for x in errorfilenames:
				
				errmsg=errmsg+x+"\n"
				
			
			print errmsg
				
			self.wtree.get_widget("labelErrorReport").set_text(errmsg)
			
			self.wtree.get_widget("windowErrReport").show()
			
		
		else:
		
			self.wtree.get_widget("windowSuccess").show()
	 	
	 	self.post_conversion()
		


		
	# # # # # # # # # # # # # # # # # # # # # # # #
	# Don't Delete Widgets When closed; Only hide #
	# # # # # # # # # # # # # # # # # # # # # # # #	
		
	def dontdelete(self,widget,dummy):
		
		
		widget.hide()
		
		return True


		
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Don't delete main window; Safe Quit after closing operations  #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # # # # #

	def dontdeleteMain(self,widget,dummy):
	
		
		self.safequit(widget)
		
		return True


	
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Hide the Error Report Window on clicking the close button #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # # #
	
	def clickederrclose(self,widget):
		
		
		self.wtree.get_widget("windowErrReport").hide()


		
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Launch the About Dialog on clicking the About button  #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # #
	
	def launchabout(self,widget):
		
		
		self.wtree.get_widget("windowAbout").show()
		

	
	
	# # # # # # # # # # # # # # # # # # # # # # #
	# Close the About Dialog on clicking Close  #
	# # # # # # # # # # # # # # # # # # # # # # #
	
	def closeabout(self,widget):
		
		
		self.wtree.get_widget("windowAbout").hide()
	
	
	
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Quit if no conversion is in progres, else ask for confirmation  #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # # # # # #	
	
	def safequit(self,widget):
		
		
		# Check if a conversion is in progress
		 
		if self.isrunning and self.fp.poll() == None:
			
			self.wtree.get_widget("windowConfirmQuit").show()
			
			print "A Conversion is in progress !! Are you sure u wan't to Quit???"
				
		
		else:
			
			exit(0)
			
			print "\n\nQuitting......\n\n"
			



	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Upon confirmation, kill the conversion in progress and Quit #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # # # #
			
	def killandquit(self,widget):
		
		
		# Kill the running process before quitting
		
		if self.isrunning and self.fp.poll() == None:
		
			self.fp.kill()
			
			self.fp.terminate()
			
			cmd=["kill","-9",str(self.fp.pid)]
			
			fp=subprocess.Popen(cmd,shell=False)
			
			
			if fp.returncode:
				
				print "Unable to kill the running conversion"
				
				
			else:
				
				print "Successfully killed the running conversion"
				
				
		print "\n\nQuitting....\n\n"
		
		exit(0)
		



	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Skip the current conversion in progress on clicking the skip button #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # # # # # # # #
	
	def skipconversion(self,widget):
		
		
		if self.isrunning and self.fp.poll() == None:
			
			self.fp.kill()
			
			self.fp.terminate()
			
			cmd=["kill","-9",str(self.fp.pid)]
				
			fp=subprocess.Popen(cmd,shell=False)
			
			if fp.returncode:
				
				print "Unable to skip the current conversion"
				
				
			else:
				
				print "Successfully skipped the current conversion"
		
	


	# # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Hide the Success Dialog on clicking the O.K button  #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # #
	
	def hidesuccess(self,widget):
		
		
		self.wtree.get_widget("windowSuccess").hide()
		
	


	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# Hide the confirmation dialog and return to the process  #
	# # # # # # # # # # # # # # # # # # # # # # # #	# # # # # #
		
	def hideconfirm(self,widget):
		
		
		self.wtree.get_widget("windowConfirmQuit").hide()
		


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# The Main Section; The part that will be run first #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
	
	go=MainLoop()
	
	return 0




if __name__ == '__main__':
	
	main()
