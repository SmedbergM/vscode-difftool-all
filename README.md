# vscode-difftool-all
Open all diffs between two commits in a single VSCode instance

## Requirements
This script requires only Python standard library modules. It invokes `git`
and `code`.

I wrote it for use on Posix systems; while it has not been tested on Windows,
it should be portable. If you encounter a bug, feel free to raise an issue
containing a minimal working example.

## Basic usage

Assuming that the current working diretory is under Git,
```sh
vscode_difftool_all.py <commit-ish> <commit-ish>
```
will find all the paths which differ between the two commits, and open the
corresponding diffs in a single instance of Visual Studio Code.

(A `<commit-ish>` is anything that `git rev-parse` can resolve: a full commit
hash, a shortened hash, a branch name, a tag, etc.)

Both versions will be written to temporary files; because the script does not
wait for VSCode to close, it is the user's responsibility to clean up any
temporary files and directories. The script will print the path of the
generated temporary directory to standard out.

If the second `<commit-ish>` is omitted, the current working tree will be
used. In this case, only the left version will be written to temporary files;
the right version will be opened from the working tree, so that edits will
persist.

## Recommended installation
It is recommended that you add a symbolic link from somewhere on your `PATH`
to the `vscode_difftool_all.py` script; for example, if `~/bin` is on your
`PATH`, then running
```sh
cd ~/bin
ln -s /path/to/vscode_difftool_all.py git-difftool-all
```
will enable invocations like
```sh
git difftool-all my-branch main
```
in any Git repository.
