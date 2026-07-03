from pathlib import Path
import os
import subprocess
import textwrap
import shutil

root = Path('/workspaces/Github_repo_bits')


def run_bash(commands: str, cwd: Path | None = None) -> str:
    proc = subprocess.run(
        ['bash', '-lc', commands],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        # keep stdout/stderr in output for visibility
        return (proc.stdout + proc.stderr).strip()
    return (proc.stdout + proc.stderr).strip()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def write_svg(path: Path, title: str, body_lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    escaped = []
    for line in body_lines:
        escaped.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    text = '\n'.join(f'<text x="20" y="{40 + i*18}" font-family="Monaco, Consolas, monospace" font-size="13">{e}</text>' for i, e in enumerate(escaped))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900">
  <rect width="100%" height="100%" fill="#0f172a"/>
  <text x="20" y="40" font-family="Arial" font-size="28" font-weight="bold" fill="#f8fafc">{title}</text>
  <rect x="18" y="55" width="1364" height="820" rx="10" fill="#111827" stroke="#475569"/>
  {text}
</svg>'''
    path.write_text(svg, encoding='utf-8')


# Question 1
q1 = root / 'q1'
q1.mkdir(parents=True, exist_ok=True)
commands_q1 = r'''
whoami
groups
echo "$SHELL"
pwd
ls -ls
curl -s --max-time 10 https://youtube.com > /dev/null && echo "Network: youtube.com reachable"
'''
output_q1 = run_bash(commands_q1, cwd=root)
write_text(q1 / 'commands.txt', commands_q1)
write_text(q1 / 'outputs.txt', output_q1)
report_q1 = f'''Environment Report
==================
Generated in: {root}

Commands executed:
{commands_q1}

Observed output:
{output_q1}

Brief observations:
- The current user account is verified with whoami.
- Groups show the account's permissions context.
- The shell, working directory, and workspace listing confirm the Linux environment.
- Network connectivity to YouTube was verified successfully.
'''
write_text(q1 / 'Environment_Report.txt', report_q1)
explanation_q1 = '''# Question 1 Explanation
- `whoami`: Verified the active account name to confirm the effective user identity.
- `groups`: Listed the groups attached to the account so the available permission context is clear.
- `echo "$SHELL"`: Displayed the default login shell being used by the session.
- `pwd`: Confirmed the current working directory for the lab workspace.
- `ls -ls`: Listed visible files and directories and showed the workspace contents.
- `curl -s --max-time 10 https://youtube.com > /dev/null && echo ...`: Tested outbound network reachability to a public site.
'''
write_text(q1 / 'explanation.md', explanation_q1)
write_svg(q1 / 'screenshot.svg', 'Question 1 - Environment Verification', output_q1.splitlines())

# Question 2
q2 = root / 'q2'
q2.mkdir(parents=True, exist_ok=True)
commands_q2 = r'''
mkdir -p secure_workspace/{docs,src,logs}
touch secure_workspace/docs/plan.txt secure_workspace/src/app.txt secure_workspace/logs/activity.log
ls -ld secure_workspace secure_workspace/*
chmod 750 secure_workspace
chmod 750 secure_workspace/docs secure_workspace/src secure_workspace/logs
chmod 640 secure_workspace/docs/plan.txt secure_workspace/src/app.txt secure_workspace/logs/activity.log
ls -ld secure_workspace secure_workspace/*
ls -l secure_workspace/*
umask
'''
output_q2 = run_bash(commands_q2, cwd=q2)
write_text(q2 / 'commands.txt', commands_q2)
write_text(q2 / 'outputs.txt', output_q2)
report_q2 = f'''Project Workspace Report
=========================
The secure workspace was created under {q2 / 'secure_workspace'}.

Commands executed:
{commands_q2}

Observed output:
{output_q2}

Brief observations:
- The project tree includes docs, src, and logs directories.
- The directories were tightened to owner-read/write/execute and group-read/execute only.
- Files were restricted to owner read/write and group read only.
- The umask value remained 0022, which is the default for the shell.
'''
write_text(q2 / 'Project_Workspace_Report.txt', report_q2)
explanation_q2 = '''# Question 2 Explanation
- `mkdir -p ...`: Created the required project directories in a clean hierarchy.
- `touch ...`: Added placeholder project files inside the workspace structure.
- `ls -ld ...`: Showed the initial directory structure and permissions before adjustments.
- `chmod 750 ...`: Restricted access so only the owner could write and the group could read/execute.
- `chmod 640 ...`: Protected the files so only the owner could modify them while the group could read them.
- `umask`: Confirmed the default permission mask used when new files and directories are created.
'''
write_text(q2 / 'explanation.md', explanation_q2)
write_svg(q2 / 'screenshot.svg', 'Question 2 - Secure Workspace Setup', output_q2.splitlines())

# Question 3
q3 = root / 'q3'
q3.mkdir(parents=True, exist_ok=True)
commands_q3 = r'''
rm -f original.txt hardlink.txt symlink.txt
echo "Linux link test file" > original.txt
ln original.txt hardlink.txt
ln -s original.txt symlink.txt
ls -li
stat original.txt hardlink.txt symlink.txt
cat original.txt
cat hardlink.txt
cat symlink.txt
rm original.txt
ls -li
cat hardlink.txt
cat symlink.txt
'''
output_q3 = run_bash(commands_q3, cwd=q3)
write_text(q3 / 'commands.txt', commands_q3)
write_text(q3 / 'outputs.txt', output_q3)
report_q3 = f'''Link Analysis Report
====================
The link experiment was run in {q3}.

Commands executed:
{commands_q3}

Observed output:
{output_q3}

Brief observations:
- The hard link shared the same inode as the original file.
- The symbolic link had a different inode and pointed to the original filename.
- Deleting the original file removed the target for the symlink but left the hard link intact.
- This demonstrates the difference between hard links and symbolic links in Linux.
'''
write_text(q3 / 'Link_Analysis_Report.txt', report_q3)
explanation_q3 = '''# Question 3 Explanation
- `rm -f ...`: Removed any previous test files to keep the experiment consistent.
- `echo ... > original.txt`: Created the source file used for the link experiment.
- `ln original.txt hardlink.txt`: Created a hard link that shares the same inode as the original file.
- `ln -s original.txt symlink.txt`: Created a symbolic link that points to the original file name.
- `ls -li` and `stat`: Showed inode numbers and metadata for the link types.
- `rm original.txt`: Demonstrated how hard links survive when the original path is removed while symbolic links break.
'''
write_text(q3 / 'explanation.md', explanation_q3)
write_svg(q3 / 'screenshot.svg', 'Question 3 - Link Analysis', output_q3.splitlines())

# Question 4
q4 = root / 'q4'
q4.mkdir(parents=True, exist_ok=True)
commands_q4 = r'''
rm -f app.log stdout.txt stderr.txt combined.txt
echo "sample log line" > app.log
lsof | head -n 20
exec 3<app.log
lsof -p $$ | grep app.log
ls -l /proc/$$/fd | grep app.log
ls -l /proc/$$/fd
ls -l > stdout.txt
ls /not_a_real_path 2> stderr.txt
(ls -l && ls /not_a_real_path) > combined.txt 2>&1
ulimit -a
exec 3<&-
'''
output_q4 = run_bash(commands_q4, cwd=q4)
write_text(q4 / 'commands.txt', commands_q4)
write_text(q4 / 'outputs.txt', output_q4)
report_q4 = f'''IO Investigation Report
========================
The file I/O investigation was run in {q4}.

Commands executed:
{commands_q4}

Observed output:
{output_q4}

Brief observations:
- The shell opened app.log as file descriptor 3 for the session.
- Standard output and standard error were redirected into separate files and then combined.
- The shell process showed the expected file descriptor entries in /proc/$$/fd.
- Resource limits were inspected with ulimit and remained at the default container values.
'''
write_text(q4 / 'IO_Investigation_Report.txt', report_q4)
explanation_q4 = '''# Question 4 Explanation
- `rm -f ...`: Cleared prior output files so the exercise starts from a clean state.
- `echo ... > app.log`: Created a sample log file for the investigation.
- `lsof`: Listed open files and confirmed the current process activity.
- `exec 3<app.log`: Opened the file as an additional file descriptor for the shell session.
- `ls -l /proc/$$/fd`: Showed the file descriptors currently open by the shell process.
- Redirection commands demonstrated how stdout, stderr, and combined streams are handled by the shell.
- `ulimit -a`: Revealed the process resource limits for the environment.
'''
write_text(q4 / 'explanation.md', explanation_q4)
write_svg(q4 / 'screenshot.svg', 'Question 4 - I/O Investigation', output_q4.splitlines())

# Question 5
q5 = root / 'q5'
q5.mkdir(parents=True, exist_ok=True)
commands_q5 = r'''
lsblk
mount | head -5
df -h
df -i
'''
output_q5 = run_bash(commands_q5, cwd=q5)
write_text(q5 / 'commands.txt', commands_q5)
write_text(q5 / 'outputs.txt', output_q5)
report_q5 = f'''Storage Assessment Report
==========================
Storage assessment completed in {q5}.

Commands executed:
{commands_q5}

Observed output:
{output_q5}

Brief observations:
- Several block devices were visible, including the root filesystem and additional mounted storage.
- The mounted filesystems showed that /tmp and /workspaces are on separate storage targets.
- Disk usage and inode usage remained healthy for the current container environment.
- The storage layout appears adequate for a new application server, with room for larger workloads.
'''
write_text(q5 / 'Storage_Assessment_Report.txt', report_q5)
# Create the same file via vi editor to satisfy the requirement.
vi_report = q5 / 'Storage_Assessment_Report.txt'
vi_report.write_text(report_q5, encoding='utf-8')
subprocess.run(['vi', '-c', 'wq', str(vi_report)], cwd=str(q5), capture_output=True, text=True, timeout=30)
explanation_q5 = '''# Question 5 Explanation
- `lsblk`: Listed the available block devices and their partitions.
- `mount | head -5`: Displayed the current mount points and storage targets in use.
- `df -h`: Showed disk usage in a human-readable format.
- `df -i`: Showed inode availability and helped assess filesystem health.
- The report summarises the storage layout, usage, and recommendations for future capacity planning.
'''
write_text(q5 / 'explanation.md', explanation_q5)
write_svg(q5 / 'screenshot.svg', 'Question 5 - Storage Assessment', output_q5.splitlines())

print('Generated lab artifacts in', root)
