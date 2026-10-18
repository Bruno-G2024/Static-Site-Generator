import os
import sys
import shutil
from gencontent import generate_pages_recursive

static_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/static'
public_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/docs'
content_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/content'
template_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/template.html'
dest_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/public/index.html'

def to_basepath():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return sys.argv[0]

def copy_directory(src, dst):
    if os.path.exists(dst):
        try:
            shutil.rmtree(dst)
            print(f'La carpeta "{public_path}" y todo su contenido ha sido eliminada con exito')
        except Exception as e:
            print(f'Ocurrio un error al intentar eliminar la carpeta: {e}')
            
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_directory(src_path, dst_path)

basepath = to_basepath()

def main():

    copy_directory(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path, basepath)

main()