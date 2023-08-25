import os
import subprocess
import shutil
from datetime import datetime, timedelta

# MySQL数据库配置
mysql_host = ' '
mysql_user = ' '
mysql_password = ' '


# 备份目录和文件名
backup_dir = '/backup/'
backup_file = f'{backup_dir}/backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.sql'
compressed_file = f'{backup_dir}/backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.sql.gz'

# 备份数据库
dump_command = f'mysqldump -h {mysql_host} -u {mysql_user} -p{mysql_password} --single-transaction --master-data=2 -A -E -R --triggers> {backup_file}'
subprocess.call(dump_command, shell=True)

# 压缩备份文件
compress_command = f'gzip {backup_file}'
subprocess.call(compress_command, shell=True)

# 删除超过7天的备份文件
current_time = datetime.now()
for file in os.listdir(backup_dir):
    file_path = os.path.join(backup_dir, file)
    if os.path.isfile(file_path):
        modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if current_time - modification_time > timedelta(days=7):
            os.remove(file_path)
