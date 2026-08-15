This script will build kobo-friendly picture 'books' in epub format, using all images in the current folder.
First it will look for duplicates by generating a hash of each image and looking for matches,
Next it will rename the pngs to a random hash name
Next it will convert, in batches of 100, images to the html needed to display those images
Next it will convert those .html files to .epub files
Finally it will move all processed .png images to the 'done' folder.  

python remove_duplicate_images.py
./random_rename_pngs.sh
./imgs2htmls.sh
./books2epubs.sh
mv *.png done
