import re

text = '<div><span class="actionBar__text"> Showing 18 of 101 products.</span></div>'
pattern = r'Showing (\d+) of (\d+) products.'
match = re.search(pattern, text)

if match:
    current = match.group(1)
    total = match.group(2)
    print("Current:", current)
    print("Total:", total)
