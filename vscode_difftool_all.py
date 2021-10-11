#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import tempfile

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=rev_parse)
    parser.add_argument("right", nargs="?", type=rev_parse)
    return parser.parse_args()

def rev_parse(rev):
    cmd = ["git", "rev-parse", "--short", rev]
    p = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return p.stdout.strip()

def list_paths(args):
    cmd = ["git", "diff", "--name-only"] + [args.left, args.right]
    cmd = list(filter(bool, cmd))
    with subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE) as p:
        for line in p.stdout:
            s = line.strip()
            if s:
                yield s

    if p.returncode:
        # The context manager waits until the process is complete, so
        # returncode should not be None
        msg = "{} returned status {}".format(" ".join(cmd), p.returncode)
        raise subprocess.SubprocessError(msg)

def main(args):
    tmp = tempfile.mkdtemp(prefix="difftool-")
    print(f"To clean up workspace, run\n    rm -rf {tmp}")

    def difftool(path, reuse_window):
        (rd, b) = os.path.split(path)
        abs_d = os.path.join(tmp, rd)
        os.makedirs(abs_d, exist_ok=True)
        left_path = os.path.join(abs_d, f"{args.left}.{b}")
        with open(left_path, "w") as left:
            cmd = ["git", "show", f"{args.left}:{path}"]
            subprocess.run(cmd, check=False, stdout=left, stderr=subprocess.DEVNULL)
        if args.right:
            right_path = os.path.join(abs_d, f"{args.right}.{b}")
            with open(right_path, "w") as right:
                cmd = ["git", "show", f"{args.right}:{path}"]
                subprocess.run(cmd, check=True, stdout=right)
        elif os.path.exists(path):
            # Then we are diffing implicitly against HEAD, and we want to edit the working tree
            right_path = path
        else:
            right_path = os.devnull
        cmd = [
            "code", "--diff",
            "-r" if reuse_window else "-n",
            left_path, right_path
        ]
        subprocess.run(cmd, check=True)

    for (idx, path) in enumerate(list_paths(args)):
        difftool(path, idx)


if "__main__" == __name__:
    args = parse_args()
    main(args)
