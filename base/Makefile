in=$1
out=$2

pdf:
	pandoc $1 \
		--from=markdown+tex_math_single_backslash+tex_math_dollars+raw_tex \
		--to=latex \
		--output=$2 \
		--pdf-engine=xelatex \
		--variable "geometry=margin=1.2in" \
		--variable "fontsize=12pt"
