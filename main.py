from ftplib import FTP
import os

# Paramètres de connexion FTP
FTP_HOST = "10.0.0.1"
FTP_USER = "anonymous"
FTP_PASS = ""
LOCAL_DIR = "./"

def get_tif_filename(files):
    # find the file with the .tif extension
    tif_files = [file for file in files if file.endswith('.tif')]
    return tif_files[0]

def get_jpg_file(files):
    jpgs = [f for f in files if f.endswith('.jpg')]
    jpgs.sort(reverse=True)
    return jpgs[0]

def download_file(ftp, filename, date, target ):
    ext = os.path.splitext(filename)[1]
    num = filename.split('-')[1].split('.')[0]
    
    exists=True
    final = 0
    print(f"    Download file : {filename}")

    while exists:
        local_filename = os.path.join(LOCAL_DIR, f"{date}_{target}_{num}_{final}{ext}")
        if not os.path.isfile(local_filename):
            exists=False
        final += 1

    with open(local_filename, "wb") as local_file:
        ftp.retrbinary(f"RETR {filename}", local_file.write)
    print(f"    File downloaded : {local_filename}")

def download_dir(ftp, date, target):
    ftp.cwd("01-images-initial")
    files = ftp.nlst()

    downloads = [get_jpg_file(files),get_tif_filename(files)]
    for filename in downloads:
        download_file(ftp, filename, date, target)

    ftp.cwd("..")

# Connexion au serveur FTP
ftp = FTP(FTP_HOST)
ftp.login(user=FTP_USER, passwd=FTP_PASS)
print(f"Connecté à {FTP_HOST}")
print(ftp.nlst())
ftp.cwd("/user")

# Liste les éléments du répertoire courant
directories = ftp.nlst()
directories.sort(reverse=False)
# Filtre les répertoires (tentative avec cwd)
print("\nRépertoires disponibles :")


for i, dir_name in enumerate(directories):
    print(f"{i + 1}. {dir_name}")

# Demander à l'utilisateur de sélectionner un répertoire
choices = input("\nSélectionnez un répertoire par son numéro : ")

for choice in choices.split(','): 
    selected_dir = directories[int(choice)-1]
    ftp.cwd(selected_dir)
    print(f"\n### Current directory : {ftp.pwd()}")

    # Liste les fichiers dans le répertoire
    files = ftp.nlst()


    # Télécharger le fichier
    tab=selected_dir.split("_")
    date=tab[0]
    target=tab[3]
    type=tab[2]


    if type=="observation":
        download_dir(ftp, date, target)
    else:
        plan_directories = ftp.nlst()
        for dir in plan_directories:
            if dir not in ['.','..']:
                target = dir.split('-')[2]
                ftp.cwd(dir)
                download_dir(ftp, date, target)
                ftp.cwd('..')
    ftp.cwd('..')

ftp.quit()
"""
local_filename = os.path.join(".", filename)
with open(local_filename, "wb") as f:
    ftp.retrbinary(f"RETR {filename}", f.write)

print(f"\nFichier téléchargé avec succès : {local_filename}")

# Fermer la connexion
ftp.quit()
"""