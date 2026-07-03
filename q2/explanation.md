# Question 2 Explanation
- `mkdir -p ...`: Created the required project directories in a clean hierarchy.
- `touch ...`: Added placeholder project files inside the workspace structure.
- `ls -ld ...`: Showed the initial directory structure and permissions before adjustments.
- `chmod 750 ...`: Restricted access so only the owner could write and the group could read/execute.
- `chmod 640 ...`: Protected the files so only the owner could modify them while the group could read them.
- `umask`: Confirmed the default permission mask used when new files and directories are created.
