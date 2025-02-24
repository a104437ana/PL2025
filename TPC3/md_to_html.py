import re
import sys

def md_to_html (md):
    md = re.sub(r'^ {0,3}#{1} +(.*)$',r'<h1>\1</h1>',md,flags=re.M)
    md = re.sub(r'^ {0,3}#{2} +(.*)$',r'<h2>\1</h2>',md,flags=re.M)
    md = re.sub(r'^ {0,3}#{3} +(.*)$',r'<h3>\1</h3>',md,flags=re.M)
    md = re.sub(r'((\*\*)+)(?=\S)(.*\S)\1',r'<b>\3</b>',md)
    md = re.sub(r'\*(?=\S)(.*\S)\*',r'<i>\1</i>',md)
    md = re.sub(r'\n( {0,3}\d+\. {1}(.*)\n)+',r'<ol>\g<0></ol>',md)
    md = re.sub(r'^ {0,3}\d+\. {1}(.*)$',r'<li>\1</li>',md,flags=re.M)
    md = re.sub(r'!\[(.*)\]\((.*)\)',r'<img src="\2" alt="\1"/>',md)
    md = re.sub(r'\[(.*)\]\((.*)\)',r'<a href="\2">\1</a>',md)
    print(md)

md_to_html(sys.stdin.read())