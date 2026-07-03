# Question 3 Explanation
- `rm -f ...`: Removed any previous test files to keep the experiment consistent.
- `echo ... > original.txt`: Created the source file used for the link experiment.
- `ln original.txt hardlink.txt`: Created a hard link that shares the same inode as the original file.
- `ln -s original.txt symlink.txt`: Created a symbolic link that points to the original file name.
- `ls -li` and `stat`: Showed inode numbers and metadata for the link types.
- `rm original.txt`: Demonstrated how hard links survive when the original path is removed while symbolic links break.
