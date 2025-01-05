import camo_lib as cammoitor
import os
def main(*args):
    cammoitor.launch(os.path.dirname(__file__),*args)

if __name__=="__main__":
    import sys
    main(sys.argv)