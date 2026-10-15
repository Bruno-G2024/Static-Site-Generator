import os
import shutil
from pathlib import Path
from split_nodes import markdown_to_html_node

static_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/static'
public_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/public'
content_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/content'
template_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/template.html'
dest_path = '/home/bruno_dev/workspace/Static Site Gen/Static-Site-Generator/public/index.html'

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

def extract_title(markdown: str) -> str:
    if not markdown.startswith('# '):
        raise Exception("The title inserted is not valid in markdown format")
    title = markdown.split('\n')
    return title[0].removeprefix('# ')

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as f:
        from_path_content = f.read()
    with open(template_path, 'r') as t:
        template_path_content = t.read()

    page_content = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)

    template_path_content = template_path_content.replace('{{ Title }}', title)
    template_path_content = template_path_content.replace('{{ Content }}', page_content)

    with open(dest_path, 'w') as f:
        f.write(template_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for item in os.listdir(dir_path_content):
        new_dir_path_content = os.path.join(dir_path_content, item)
        new_des_dir_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(new_dir_path_content):
            new_des_dir_path = Path(new_des_dir_path)
            with open(new_dir_path_content, 'r') as f:
                from_path_content = f.read()
            with open(template_path, 'r') as t:
                template_path_content = t.read()
            
            page_content = markdown_to_html_node(from_path_content).to_html()
            title = extract_title(from_path_content)
            
            template_path_content = template_path_content.replace('{{ Title }}', title)
            template_path_content = template_path_content.replace('{{ Content }}', page_content)
            
            with open(new_des_dir_path.with_suffix('.html'), 'w') as f:
                    f.write(template_path_content)
        else:
            os.makedirs(new_des_dir_path, exist_ok=True)
            generate_pages_recursive(new_dir_path_content, template_path, new_des_dir_path)

def main():

    copy_directory(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)
    #generate_page(content_path, template_path, dest_path)
    # new_static_img = os.path.join(static_path, static_img_path)
    # new_static_css = os.path.join(static_path, static_css_path)

    # if os.path.exists(public_path):
    #     try:
    #         shutil.rmtree(public_path)
    #         print(f'La carpeta "{public_path}" y todo su contenido ha sido eliminada con exito')
    #     except Exception as e:
    #         print(f'Ocurrio un error al intentar eliminar la carpeta: {e}')

    # os.mkdir(public_path)
    # os.mkdir(public_path + '/images')

    # shutil.copy(new_static_img, public_path +'/images')
    # shutil.copy(new_static_css, public_path)
    
    #return file_list

main()