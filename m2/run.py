from viewer import Viewer
from ck import CK
from renderer import Renderer
import json
import sys
if __name__ == '__main__':

    if len(sys.argv) > 1:
        fn = sys.argv[1]
        with open(fn) as data_file:
            data = json.load(data_file)
            ck = CK(data['program'])
            renderer = Renderer(ck)
            viewer = Viewer(renderer, 60, data['output'])
    else:
        ck = CK()
        renderer = Renderer(ck)
        viewer = Viewer(renderer, 60)
