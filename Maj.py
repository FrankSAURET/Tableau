import os
import requests
import zipfile
import shutil
import inkex

__version__ = "2024.2"

REPO = "https://github.com/FrankSAURET"
INKSCAPE_EXT_DIR = os.path.join(os.getenv('APPDATA'), 'inkscape', 'extensions')
CUR_FOLDER=os.path.dirname(os.path.realpath(__file__))

def download_files(url, download_path):
    response = requests.get(url)
    with open(download_path, 'wb') as file:
        file.write(response.content)

def copier_fichiers_avec_nom(source_dir, dest_dir, nom_fichier_sans_extension):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if nom_fichier_sans_extension in file:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                shutil.copy2(source_file, dest_file)
                print(f"Copié : {source_file} -> {dest_file}")            

def lister_fichiers_inx_avec_chaine(repertoire, chaine):
    fichiers_correspondants = []
    for root, dirs, files in os.walk(repertoire):
        for file in files:
            if file.endswith('.inx'):
                chemin_complet = os.path.join(root, file)
                with open(chemin_complet, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                    if chaine in contenu:
                        nom_fichier_sans_extension = os.path.splitext(file)[0]
                        fichiers_correspondants.append((nom_fichier_sans_extension))
    return fichiers_correspondants

def extraire_zip(zip_path, extract_to):
    if not os.path.exists(zip_path):
        return
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def mise_a_jour():
    fichiers = lister_fichiers_inx_avec_chaine(CUR_FOLDER, 'franksauret')
    for fichier in fichiers:
        if fichier not in 'Mij': # Ne pas mettre à jour les fichiers Mij [ cette fonction est donc désactivée pour l'instant]
            nomzip=f"{fichier}.zip"
            download_path = os.path.join(os.getenv('TEMP'),nomzip)
            extract_path = os.path.join(os.getenv('TEMP'),'extension_extract')
            NomRepoGithub = f"{REPO}/{fichier}/archive/refs/heads/main.zip"
            download_files(NomRepoGithub, download_path)
            # Extraire le fichier ZIP
            extraire_zip(download_path, extract_path)
            # Copier les fichiers dont le nom contient nom_fichier_sans_extension
            copier_fichiers_avec_nom(extract_path, CUR_FOLDER, fichier)
            # Clean up
            os.remove(download_path)
            shutil.rmtree(extract_path)
        
def main():
    mise_a_jour()

if __name__ == "__main__":
    main()