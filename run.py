from viewer import Viewer
from ck import CK
from renderer import Renderer

if __name__ == '__main__':

    ck = CK()
    renderer = Renderer(ck)
    viewer = Viewer(renderer, 30)
