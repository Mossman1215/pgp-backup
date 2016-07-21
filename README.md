# pgp-backup
encrypted python backup scripts using gnupg
EncryptedUploader is the main module and will upload a directory to a folder in google drive. 
Options.conf defines where the oauth credentials folder lives and where to store temp files
In order to run this script it should be run as a service so that it isn't halted mid upload.
--Some sort of link to systemd docs

upload_dir is an unencrypted uploader script

# Limits on API Calls
Each google account should be related to a google api project so that they don't overload a single api project's limits.
1000000 requests/100sec
1000000000/24hrs

Referencing GDrive tutorials
Jeremy Blythe
https://github.com/jerbly/tutorials/tree/master/motion
http://jeremyblythe.blogspot.com/2015/06/motion-google-drive-uploader-for-oauth.html