#!/usr/bin/env python3
"""Remove duplicate images in the current directory by hashing image content.

This script prefers to hash normalized pixel data using Pillow when available
so duplicates with different metadata or file containers are detected. If
Pillow is not installed it falls back to hashing the raw file bytes.

Usage:
  python remove_duplicate_images.py [--dry-run] [--verbose]

Options:
  -n, --dry-run   Show what would be removed without deleting files.
  -v, --verbose   Print kept files and extra information.
  -e, --extensions Comma-separated list of extensions to consider (default: jpg,jpeg,png,gif,webp,bmp,tiff)
"""

import os
import sys
import hashlib
import argparse

try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def image_hash(path: str) -> str:
    if not PIL_AVAILABLE:
        return file_hash(path)

    try:
        with Image.open(path) as img:
            img = img.convert('RGBA')
            w, h = img.size
            mode = img.mode
            data = img.tobytes()
            hh = hashlib.sha256()
            hh.update(f"{w}x{h}|{mode}".encode('utf-8'))
            hh.update(data)
            return hh.hexdigest()
    except Exception:
        # If PIL can't open/normalize, fall back to raw bytes
        return file_hash(path)


def find_images(exts):
    files = []
    for name in sorted(os.listdir('.')):
        if not os.path.isfile(name):
            continue
        low = name.lower()
        for ext in exts:
            if low.endswith(ext):
                files.append(name)
                break
    return files


def main():
    parser = argparse.ArgumentParser(description='Remove duplicate images in current directory')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Do not delete files; just show actions')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-e', '--extensions', default='jpg,jpeg,png,gif,webp,bmp,tiff', help='Comma-separated extensions (no dots)')
    args = parser.parse_args()

    exts = tuple('.' + e.strip().lower() for e in args.extensions.split(',') if e.strip())

    images = find_images(exts)
    if not images:
        print('No image files found in current directory.')
        return

    if not PIL_AVAILABLE:
        print('Pillow not available — falling back to raw file hashing. Install Pillow for better duplicate detection: pip install pillow', file=sys.stderr)

    seen = {}
    for path in images:
        h = image_hash(path)
        if h in seen:
            first = seen[h]
            if args.dry_run:
                print(f'DUPLICATE (would remove): {path}  — same as {first}')
            else:
                try:
                    os.remove(path)
                    print(f'Removed duplicate: {path}  — same as {first}')
                except Exception as exc:
                    print(f'Failed to remove {path}: {exc}', file=sys.stderr)
        else:
            seen[h] = path
            if args.verbose:
                print(f'Keeping: {path}')


if __name__ == '__main__':
    main()
