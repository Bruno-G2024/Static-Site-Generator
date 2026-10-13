import os
import shutil
from textnode import TextNode, TextType

static_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/static'
static_img_path = 'images/tolkien.png'
static_css_path = 'index.css'
public_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/public'

def file_list(path):
    return os.listdir(path)

def main():

    new_static_img = os.path.join(static_path, static_img_path)
    new_static_css = os.path.join(static_path, static_css_path)

    if os.path.exists(public_path):
        try:
            shutil.rmtree(public_path)
            print(f'La carpeta "{public_path}" y todo su contenido ha sido eliminada con exito')
        except Exception as e:
            print(f'Ocurrio un error al intentar eliminar la carpeta: {e}')

    os.mkdir(public_path)
    os.mkdir(public_path + '/images')

    shutil.copy(new_static_img, public_path +'/images')
    shutil.copy(new_static_css, public_path)
    
    #return file_list

main()