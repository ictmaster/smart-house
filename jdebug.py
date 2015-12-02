import sys
is_debug = True
if 'nodebug' in sys.argv:
    is_debug = False
    print("-------------IN RELEASE MODE-------------")