import os
from pathlib import Path
from split_nodes import markdown_to_html_node

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

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
            template_path_content = template_path_content.replace('href="/', f'href="{basepath}')
            template_path_content = template_path_content.replace('src="/', f'src="{basepath}')
            
            with open(new_des_dir_path.with_suffix('.html'), 'w') as f:
                    f.write(template_path_content)
        else:
            os.makedirs(new_des_dir_path, exist_ok=True)
            generate_pages_recursive(new_dir_path_content, template_path, new_des_dir_path, basepath)