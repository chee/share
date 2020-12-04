#!/usr/bin/env python3
import argparse
import mimetypes
from subprocess import PIPE
import sys
import magic
import subprocess
import os
from slugify import slugify
from .getseq import getseq

def main():
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
	source = None

	if args.file.startswith("/tmp/.psub") or args.file.startswith("/dev/fd"):
		source = args.file
		prefix = getseq()
		head = open(args.file, "rb").read(2048)
		ext = mimetypes.guess_extension(magic.from_buffer(head, True))
		output_filename = f"{prefix}{ext}"
	elif args.file.startswith("https://") or args.file.startswith("http://"):
		source = f"/tmp/{getseq()}.html"
		with open(source, "t+w") as file:
			file.write(f"""<!doctype html><meta http-equiv="refresh" content="0;url={args.file}"><a href="{args.file}">{args.file}</a>""")

		output_filename = "index.html"
	else:
		source = args.file
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
		source,
		f"{ssh_target}:{destdir}/{output_filename}"
	], stdout=PIPE)

	output = f"{args.public_root}/{dirname}/"
	if output_filename is not "index.html":
		output += output_filename
	print(output)


if __name__ == "__main__":
	sys.exit(main())
