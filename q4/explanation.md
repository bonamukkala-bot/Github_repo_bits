# Question 4 Explanation
- `rm -f ...`: Cleared prior output files so the exercise starts from a clean state.
- `echo ... > app.log`: Created a sample log file for the investigation.
- `lsof`: Listed open files and confirmed the current process activity.
- `exec 3<app.log`: Opened the file as an additional file descriptor for the shell session.
- `ls -l /proc/$$/fd`: Showed the file descriptors currently open by the shell process.
- Redirection commands demonstrated how stdout, stderr, and combined streams are handled by the shell.
- `ulimit -a`: Revealed the process resource limits for the environment.
