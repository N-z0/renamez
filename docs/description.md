![Logo icon](contents/logo/logo.svg "Software-name logo")
# Renamez
**Names Cleaner**


## ℹ️ Description
You may need to use this program to clean up file and directory names.  
Because normally all systems should handle *UTF8* names correctly,  
But not the old *FAT* system and not all clouds/backup services.  
And the distinction between lowercase and uppercase is not always made.  
Also, some local programs misinterpret names containing special characters.  
Or maybe you just need easier reading and memorizing of names.  

 - mode:'check'  
	Print pathnames of not correct names otherwise nothing.  
 - mode:'return'  
	Returns a new correct name or the same name.  
 - mode:'write'  
	Change the name on the disk if necessary.  


## 📝 Note
 - This software works by Command Line Interface (CLI).  
 - Have been tested mostly on Linux system but may operate on others compatible platforms.  
 - But it's not guaranteed without bugs and any futures improvements are not sure.  
 - Length restriction of names and extensions may vary depending on the operating system:  
	 - 8 characters for the name and 3 for the extension under DOS and Windows 3.1  
	 - 256 characters for name and extension under Windows 95, 98 and NT  
	 - 256 characters as well on Unix systems  
 - dots are extension markers, it can cause bug if a name includes a series of dots.  
	(currently this program not consider names with a prefix dot for hiding)  
 - There is no minimum restriction on numbers of extensions.  
	Names with less or no extension are considered correct even if maximum ext parameter is set higher.  


## 📜 History
- Projet made by [N-z0](mailto:syslog@laposte.net) in 2020, Because nothing else corresponded to his needs.  

