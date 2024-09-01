import os
import subprocess
import boto3
from datetime import datetime

# Defina variáveis
DB_NAME = "testdb"
DB_USER = "postgres"
DB_HOST = "172.31.86.51"
DB_PASSWORD = "5ffc0a32"
BACKUP_PATH = "/home/ubuntu/backups" #cria um diretorio para armazenar o arquivo de backup temporáriamente
S3_BUCKET = "backuppostgrezabbix "
FILENAME = f"{DB_NAME}_{datetime.now().strftime('%Y-%m-%d')}.backup"

# Exporte a senha do banco de dados
os.environ["PGPASSWORD"] = DB_PASSWORD

# Comando para criar o backup
backup_command = [
    "pg_dump", "-h", DB_HOST, "-U", DB_USER, "-d", DB_NAME,
    "-F", "c", "-b", "-v", "-f", os.path.join(BACKUP_PATH, FILENAME)
]

# Execute o comando de backup
subprocess.run(backup_command, check=True)

# Envie o backup para o S3
s3 = boto3.client('s3')
s3.upload_file(os.path.join(BACKUP_PATH, FILENAME), S3_BUCKET, FILENAME)

# Remova o arquivo de backup local (opcional)
os.remove(os.path.join(BACKUP_PATH, FILENAME))
