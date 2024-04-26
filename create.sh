# name=$1
name=$(date +%g_%U)
difficulty=6

outdir="/media/fileserver/01_users/Janik/weekly_python_challenge/$name"
#kata=$(python base/random_kata.py --kyu $difficulty) && echo "$kata" > instructions/${name}.md || exit 1;
#echo kata successfully downloaded

examples=$(grep '>>>' -A 1 instructions/${name}.md)

mkdir -p $outdir
python base/replace.py instructions/${name}.md \
        | sed "s/_NUMBER_/"$name"/" > $outdir/solution.py

pandoc instructions/${name}.md \
        --from=markdown+tex_math_single_backslash+tex_math_dollars+raw_tex+table_captions \
        --to=latex \
        --output=$outdir/instructions.pdf \
        --pdf-engine=xelatex \
        --variable "geometry=top=2.97cm" \
        --variable "geometry=bottom=2.97cm" \
        --variable "geometry=left=2.1cm" \
        --variable "geometry=right=2.1cm" \
        --variable "fontsize=12pt"

echo exercise successfully created
