#!/bin/zsh

curl 'https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt' > robots-list.txt
{
    head -n 18 static/robots.txt
    cat robots-list.txt
} > tmp.txt
echo '' >> tmp.txt
echo 'Sitemap: https://dunnodowhat.com/sitemap.xml' >> tmp.txt
mv tmp.txt static/robots.txt
rm robots-list.txt