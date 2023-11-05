#!/bin/bash

if ! tmp=$(mktemp -d); then
  echo >&2 "Failed to create tempdir"
fi
echo >&2 "Using tempdir: $tmp"

mkdir -p static/img/people

for markdown in content/_generated/people/*.md; do
  basename=$(basename -s .md "$markdown")
  url=$(perl -ne 'if (/src="(.*)"/) {print "$1\n"}' "$markdown")
  if [[ ! $url ]]; then
    echo >&2 "Failed to find URL in $basename"
    continue
  fi
  image=static/img/people/$basename.jpg
  if [[ ! -e $image ]]; then
    if ! downloaded=$(curl -# --output-dir "$tmp" -O -w '%{filename_effective}\n' "$url"); then
      echo >&2 "Failed to download image for $basename"
      continue
    fi
    if ! convert "$downloaded" -scale 600x600 -quality 92 "$image"; then
      echo >&2 "Failed to convert downloaded image for $basename"
    fi
  fi
done
