#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob

for html_file in book*.html; do
    epub_file="${html_file%.html}"
    title_name="${html_file%.html}"

    echo "Converting: $html_file -> ${epub_file}.epub"

    ebook-convert "$html_file" "${epub_file}.epub" \
        --no-chapters-in-toc \
        --title "Family Photos - $title_name" \
        --authors "Scott" \
        --margin-left 0 \
        --margin-right 0 \
        --margin-top 0 \
        --margin-bottom 0
done
