I like e-ink photo frames.  I wanted to setup a photo album and place a kobo clara colour on a stand on the main bathroom sink, and have the kids be in charge of changing the daily picture.  It gives them a feeling of some power since they get to pick the photos and is something they enjoy.

Prerequisites: 
* calibre and calibre's command-line tools
* python and bash
* On kobo 'more settings...Energy Saving': 
change 'Automatically go to sleep after' to 'Never'
change 'Automatically power off after' to 'Never'


I started out using tips found in
https://www.reddit.com/r/kobo/comments/158p6k0/ps_you_can_absolutely_set_a_nice_image_as_a/
But later decided I wanted to see these photos with the backlighting ON.
It worked far better than I expected.  With the brightness turned down to about 1/3, I get about a week of display time before I have to recharge the device.


1. Capture 3:4 areas of your favorite photos
--------------------------------------------

I used AI to create a java program that allows the user to capture a 3:4 area of the screen.  This allows you to look at family photos and for each photo, start the selection process (on windows) by entering CTRL-ALT-K, then select area, then CTRL-ALT-K again to save that selected region to the downloads folder with the prefix ScreenSnap_ and the suffix .png which is a kobo requirement.

https://github.com/sbrodsky/screensnap

use 'build.bat' to compile the code, and use 'screensnap.bat' to run the program.  Minimize the window and start selecting images from your photo album.

I transfer these images to a folder on my LAN that my Raspberry Pi has mounted.



2. Convert these 3:4 aspect ratio .png images to 1072x1448 pixels
-----------------------------------------------------------------

For all following steps, I am using a raspberry pi.

I use 'kobo_process_images.py' in a cron entry to resize all images to 1072x1448 (and perform some additional processing features during the conversion).  The python code conversion line is:

    command = [
         "magick",
         str(src),
         "-auto-orient",
         "-background",
         "white",
         "-alpha",
         "remove",
         "-alpha",
         "off",
         "-resize",
         "1072x1448!",
         str(dst),
    ]

3. Run 'runme_build_epubs.sh' which will randomize filenames, create .html files, and then build epubs using the html files and the images.

I chose to randomize the images, you may want to skip that step.  The reason I did this is because I was finding, for example, too many back-to-back images of the same 'event' and wanted more randomness when switching to the next image.

runme_build_epubs.sh:
This script will build kobo-friendly picture 'books' in epub format, using all images in the current folder.
First it will look for duplicates by generating a hash of each image and looking for matches,
Next it will rename the pngs to a random hash name
Next it will convert, in batches of 100, images to the html needed to display those images
Next it will convert those .html files to .epub files
Finally it will move all processed .png images to the 'done' folder.  

python remove_duplicate_images.py  ;generates a hash based on each file's contents and deletes if already present in another filename
./random_rename_pngs.sh            ;generates a random hash and renames each file the hashname
./imgs2htmls.sh                    ;
./books2epubs.sh                   ;
mv *.png done                      ;make sure you have a 'done' folder first!

4. Bring the .epubs into Calibre and transfer them to the Kobo clara colour.   


Addendum - I also like to surf facebook and pinterest and when I find a cool family-friend comic or quote/advice, I save those images and add them as well.  This is another example of why the randomness feature was added.

