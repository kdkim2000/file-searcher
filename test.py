import re
line = """pop = st.popover("Button label")
"""
regex_pattern="st"
print(re.search(regex_pattern, line))