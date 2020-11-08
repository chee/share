#!/usr/bin/env python3
import argparse
import mimetypes
from subprocess import PIPE
import magic
import subprocess
import os
from slugify import slugify
from .getseq import getseq

parser = argparse.ArgumentParser()
parser.add_argument(
	"file",
	help="the file to upload to the server"
)
parser.add_argument(
	"-s",
	"--server",
	help="ssh server",
	default="snoot.club"
)
parser.add_argument(
	"-u",
	"--user",
	help="ssh user",
	default="share"
)
parser.add_argument(
	"-d",
	"--server-root",
	help="directory root",
	default="/snoots/share/share.snoot.club/website"
)
parser.add_argument(
	"-p",
	"--public-root",
	help="the prefix for the public url",
	default="https://share.snoot.club"
)

args = parser.parse_args()

mimetypes.init()

if args.file.startswith("/tmp/.psub") or args.file.startswith("/dev/fd"):
	prefix = getseq()
	head = open(args.file, "rb").read(2048)
	ext = mimetypes.guess_extension(magic.from_buffer(head, True))
	output_filename = f"{prefix}{ext}"
else:
      [name, ext] = os.path.splitext(os.path.basename(args.file))
      output_filename = f"{slugify(name)}{ext}"

dirname = getseq()

ssh_target = f"{args.user}@{args.server}"

destdir = f"{args.server_root}/{dirname}"
subprocess.run(["ssh", ssh_target, "mkdir", "-p", destdir])
subprocess.run([
	"rsync",
	"-zL",
	"--progress",
	"--chmod=a+rw",
	args.file,
	f"{ssh_target}:{destdir}/{output_filename}"
], stdout=PIPE)

print(f"{args.public_root}/{dirname}/{output_filename}")
