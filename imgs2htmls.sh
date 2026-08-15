#!/usr/bin/env bash
set -euo pipefail

#  batch images into files of up to 100 images and produce book1.html, book2.html, etc.

template_path="photo_album_template2.html"
marker="<!-- your original content goes here -->"

template_html="$(<"$template_path")"
prefix=""
suffix=""
found_marker=0

while IFS= read -r line || [[ -n "$line" ]]; do
  if (( found_marker )); then
    suffix+="$line"$'\n'
    continue
  fi

  prefix+="$line"$'\n'

  if [[ "${line,,}" == "$marker" ]]; then
    found_marker=1
  fi
done <<< "$template_html"

if (( ! found_marker )); then
  echo "Marker not found in $template_path: <!-- Your original content goes here -->" >&2
  exit 1
fi

batch_size=100
shopt -s nullglob nocaseglob
files=( *.jpg *.jpeg *.png *.gif *.webp )

if (( ${#files[@]} == 0 )); then
  echo "No image files found." >&2
  exit 1
fi

file_index=1
for ((i=0; i<${#files[@]}; i+=batch_size)); do
  out="book${file_index}.html"
  {
    printf '%s' "$prefix"
    for f in "${files[@]:i:batch_size}"; do
      printf '<div class="page"><div class="full-bleed"><img src="%s"/><br>\n</div></div>\n' "$f"
    done
    printf '%s' "$suffix"
  } > "$out"
  echo "Wrote $out"
  ((file_index++))
done

shopt -u nocaseglob
