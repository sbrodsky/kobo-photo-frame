for f in *.png; do
  [[ -e "$f" ]] || continue
  new="$(openssl rand -hex 4)_$f"
  mv -- "$f" "$new"
done
