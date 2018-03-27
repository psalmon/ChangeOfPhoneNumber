import re
import os

def main():
    identify_numbers()


def identify_numbers():
    #egrep is brutally slow. We could potentially speed this up with a different regex on a regular grep
    #regex pulled and modified from: https://stackoverflow.com/a/48826
    regex = "\"(([a-zA-Z0-9]{1,2}.)?[[a-zA-Z0-9]{3}.{0,1}[[a-zA-Z0-9]{3}.{0,1}[[a-zA-Z0-9]{4})\""
    matches = os.popen('egrep ' + regex + ' /var/www -R --include=\'*.html\'').read()
    matches_formatted = matches
    matches_formatted[:] = [format_dashes(x) for x in matches]
    i = 0
    for m in matches:
        os.system('find /var/www -regex \'*.html\' -exec sed -i s/' + m + '/' + matches_formatted[i])
        i += 1


def format_dashes(raw_num):
    if not all(str(s).isdigit() for s in raw_num):
        raw_num = convert_alpha(raw_num)
    num = re.sub("[^0-9]", "", raw_num)
    if num[0] == 1:
        num = num[1:]#ignore preceeding '1'
        if len(num) == 10:
            num = "%s-%s-%s" % (num[:3],num[3:6],num[6:])
    return num


def convert_alpha(raw_num):
    #good snippet from here https://stackoverflow.com/a/23332621
    try:
        translationdict = str.maketrans("abcdefghijklmnopqrstuvwxyz", "22233344455566677778889999")
    except AttributeError:
        import string
        translationdict = string.maketrans("abcdefghijklmnopqrstuvwxyz", "22233344455566677778889999")

    out_str = raw_num.lower().translate(translationdict)
    return out_str
