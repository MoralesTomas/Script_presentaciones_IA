import os
import requests
from bs4 import BeautifulSoup
import img2pdf
import shutil

# URL base de la página web
#http://www.kunusoft.com/slides/ia1/ia102_agentes/index.php?pic= --> ejemplo de la base


diccionario = {
    "Lección 1. Introducción a la inteligencia artificial.pdf": "http://kunusoft.com/slides/ia1/ia101_intro/",
    "Lección 2. Agentes inteligentes y búsquedas.pdf": "http://kunusoft.com/slides/ia1/ia102_agentes/",
    "Lección 3. Otras búsquedas no informadas.pdf": "http://kunusoft.com/slides/ia1/ia103_otras/",
    "Lección 4. Búsquedas informadas.pdf": "http://kunusoft.com/slides/ia1/ia104_informadas/",
    "Lección 5. Búsquedas por adversario.pdf": "http://kunusoft.com/slides/ia1/ia105_adversario/",
    "Lección 6. Algoritmos genéticos.pdf": "http://kunusoft.com/slides/ia1/ia106_geneticos/",
    "Lección 7. Machine Learning I.pdf": "http://kunusoft.com/slides/ia1/ia107_ml1/",
    "Lección 8. Machine Learning II.pdf": "http://kunusoft.com/slides/ia1/ia108_ml2/",
    "Lección 9. Machine Learning III.pdf": "http://kunusoft.com/slides/ia1/ia109_ml3/",
    "Lección 10. Machine Learning IV.pdf": "http://kunusoft.com/slides/ia1/ia110_ml4/"
}

# Directorio para guardar las imágenes
image_dir = "imagenes"
os.makedirs(image_dir, exist_ok=True)

# Función para eliminar el contenido de la carpeta de imágenes
def clear_image_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"No se pudo eliminar {file_path}. Razón: {e}")

# Función para descargar una imagen dada la URL
def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Descargada {file_path}")
    else:
        print(f"No se pudo descargar la imagen desde {url}")


def descargar_presentaciones():

    global diccionario

    for pdf_name, base in diccionario.items():
        
        # Limpiar la carpeta de imágenes
        clear_image_dir(image_dir)

        base_url = f'''{ base }/index.php?pic='''


        # Obtener el número total de imágenes
        response = requests.get(base_url + "0")
        soup = BeautifulSoup(response.text, 'html.parser')
        image_info = soup.find('div', class_='image_info').get_text(strip=True)
        total_images = int(image_info.split('/')[1].split(']')[0])

        # Bucle para recorrer todas las imágenes
        for i in range(total_images + 1):
            page_url = base_url + str(i)
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tag = soup.find('div', class_='image').find('img')
            img_url = base + img_tag['src']
            img_path = os.path.join(image_dir, f"Diapositiva{i:02d}.jpg")
            download_image(img_url, img_path)

        # Generar un archivo PDF con todas las imágenes descargadas
        with open(pdf_name, "wb") as f:
            image_paths = [os.path.join(image_dir, f"Diapositiva{i:02d}.jpg") for i in range(total_images + 1)]
            f.write(img2pdf.convert(image_paths))

        print("PDF generado como", pdf_name)

descargar_presentaciones()