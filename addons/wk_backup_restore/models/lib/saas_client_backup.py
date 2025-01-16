# curl -X POST -F 'master_pwd=abcd' -F 'name=xyz' -F 'backup_format=zip' -o /path/xyz.zip http://localhost:8069/web/database/backup
import requests
import argparse
import os
import datetime
import psycopg2
import paramiko
import subprocess
from urllib.parse import urlparse
import json




class BackupStorage():
    def __init__(self):
        self.client_url = ""
        self.ssh_obj = None
        self.saas_ssh_obj = None
        self.msg = ""
        self.filename = ""
        self.backup_time = None
        self.backup_file_path = ""
        self.remote_backup_file_path = ""
        self.temp_backup_file_path = ""
        
    def init_parser(self):
        """
            Method to initialize parser for command line arguments,
            and return parser object.
        """
        parser = argparse.ArgumentParser(description='Process some arguments.')
        parser.add_argument('--mpswd', action='store',
                            help='Master password Odoo')
        parser.add_argument('--url', action='store',
                            help='saas client url')
        parser.add_argument('--dbname', action='store',
                            help='name of database to backup')
        parser.add_argument('--maindb', action='store',
                            help='name of main database')
        parser.add_argument('--dbuser', action='store',
                            help='username of main database')
        parser.add_argument('--dbpassword', action='store',
                            help='password of main database')
        parser.add_argument('--processid', action='store',
                            help='process id')
        parser.add_argument('--bkploc', action='store',
                            help='backup location local, dedicated, s3')
        parser.add_argument('--path', action='store',
                            help='Backup Path')
        parser.add_argument('--backup_format', action='store',
                            help='Backup Type')
        
        parser.add_argument('--rhost', action='store',
                    help='Remote Hostname')
        parser.add_argument('--rport', action='store',
                    help='Remote Port')
        parser.add_argument('--ruser', action='store',
                    help='Remote User')
        parser.add_argument('--rpass', action='store',
                    help='Remote Password')
        
        parser.add_argument('--temp_bkp_path', action='store',
                    help='Temporary Backup Directory')
        
        # Arguments related to SaaS Kit Backup module
        parser.add_argument('--is_remote_client', action='store',
                    help='Is Remote SaaS Client')
        

        return parser
    
    def database_entry(self, main_db, db_user, db_password, db_name, file_name, process_id, file_path, url, backup_date_time, status, message, kwargs={}):
        """
            Method to insert created backup details in the database.
        """
        try:
            if db_user == "False" or db_password == "False":
                connection = psycopg2.connect(database=main_db)
            else:
                connection = psycopg2.connect(user=db_user, password=db_password, host="127.0.0.1", port="5432", database=main_db)
        except Exception as e:
            print(e)
            print('Exited')
            exit(0)

        try:
            file_path = file_path.replace('//', '/')
            url = url.replace('//', '/')
            # Connect to database
            QUERY = "INSERT INTO backup_process_detail (name, file_name, backup_process_id, file_path, url, backup_date_time, status, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            RECORD = (db_name, file_name, process_id, file_path, url, backup_date_time, status, message)
            cursor = connection.cursor()
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute(QUERY, RECORD)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted")
        except Exception as e:
            print(e)
        finally: 
            if connection:
                cursor.close()
                connection.close()
                print("Postgresql Connection Closed")
    
    def login_backup_remote(self, args):
        """
            Method to login to remote backup server.
        """
        try:
            ssh_obj = paramiko.SSHClient()
            ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_obj.connect(hostname=args.rhost, username=args.ruser, password=args.rpass,port=args.rport)
            self.ssh_obj = ssh_obj
        except Exception as e:
            print("Couldn't connect to remote backup server.", e)
            raise Exception("Couldn't connect to remote backup server.")
            
    def execute_on_remote_shell(self, ssh_obj,command):
        """
            Method to execute commands on shell of remote server. 
        """
        response = dict()
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_obj.exec_command(command)
            print("execute_on_remote_shell out: ")
            res = ssh_stdout.readlines()
            print(res)
            print("execute_on_remote_shell err: ")
            err = ssh_stderr.readlines()
            print(err)
            if err:
                raise Exception(err)
            response['status'] = True
            response['result'] = res
            return response
        except Exception as e:
            print("+++ERROR++",command)
            print("++++++++++ERROR++++",e)
            response['status'] = False
            response['message'] = e
            return response
    
    def check_remote_backup_path(self, args, backup_dir):
        """
            Method to check remote backup path.
        """
        response = dict(status=False)
        try:
            self.login_backup_remote(args)
            cmd = "ls %s"%(backup_dir)
            check_path = self.execute_on_remote_shell(self.ssh_obj ,cmd)
            if check_path and not check_path.get('status'):
                print("Error while checking the path of remote directory - ", check_path.get('message'))
                raise Exception("Error while checking the path of remote directory - "+check_path.get('message'))
            if check_path and not check_path.get('result'):
                cmd = "mkdir -p %s; chmod -R 777 %s"%(backup_dir, backup_dir)
                upd_permission = self.execute_on_remote_shell(self.ssh_obj,cmd)
                if upd_permission and not upd_permission.get('status'):
                    print("Error while creating directory and updating permissions - ", check_path.get('message'))
                    raise Exception("Cannot create remote directory and update permissions.")
            response.update(status=True)
        except Exception as e:
            print("Error: Creating Backup Directory")
            response.update(message=e)
        return response
    
    def create_client_url(self, url):
        """
            Method to create client url for creating the backups.
        """
        client_url = ""
        if urlparse(url).scheme not in ['http','https']:
            client_url = 'http://' + url + \
                ('/' if url[-1] != '/' else '')
        else:
            client_url = url + ('/' if url[-1] != '/' else '')
        
        client_url += 'saas/database/backup'
        return client_url
    
    
    def store_backup_file(self, args, kwargs):
        """
            Method to store backup file on the local server in the mentioned path.
        """
        res = dict(status=False)
        data = {
            'master_pwd': args.mpswd,
            'name': args.dbname,
            'backup_format': args.backup_format or "zip"
        }
        
        client_url = self.client_url
        backup_dir = kwargs.get('backup_dir')
        try:
            filename = None
            backup_time = None
            backup_file_path = None
            with requests.post(client_url, data=data, stream=True) as response:
                response.raise_for_status()
                filename = response.headers.get('Backup-Filename', '')
                backup_time = response.headers.get('Backup-Time', datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S"))
                backup_file_path = os.path.join(backup_dir, filename)

                if response.headers.get('Content-Disposition'):
                    with open(backup_file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                else:
                    raise Exception(response.content.decode())

            msg = 'Database Backup Successful at ' + str(backup_time)
            res.update(status=True, filename=filename, backup_time=backup_time, backup_file_path=backup_file_path)
        except Exception as e:
            res.update(message=e)
        
        return res
            
    
    def manage_backup_files(self, args):
        """
            Method to manage the backup files on either local server or remote server or any cloud server
        """
        vals = dict()
        backup_dir = os.path.join(args.path, 'backups')
        response = dict(status=False)
        self.client_url = self.create_client_url(args.url)
        try:
            vals.update(backup_dir=backup_dir)
            backup_location = args.bkploc
            if hasattr(self,'_create_%s_backup'%backup_location):## if you want to update dictionary then you can define this function _call_{backup_location}_backup_script
                response = getattr(self,'_create_%s_backup'%backup_location)(args, vals)
                
            msg = 'Database Backup Successful at ' + str(self.backup_time)
            self.database_entry(args.maindb, args.dbuser, args.dbpassword, args.dbname, self.filename, args.processid, backup_dir+'/', self.backup_file_path, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="Success", message=msg)
            response.update(status=True, message=msg)
        except Exception as e:
            msg = 'Failed at ' + str(self.backup_time or datetime.datetime.now()) + ' ' + str(e)
            self.database_entry(args.maindb, args.dbuser, args.dbpassword, args.dbname, self.filename, args.processid, backup_dir+'/', self.backup_file_path if self.backup_file_path else self.remote_backup_file_path if self.remote_backup_file_path else '', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="Failure", message=msg)
            response.update(status=False, message=msg)
        
        return response
    

    def _create_local_backup(self, args, vals):
        """
            Method to create backup on local server.
            It copies the local backup file to remote saas server.
        """
        response = dict(status=False)
        temp_backup_dir = None
        backup_dir = vals.get('backup_dir')
        if not os.path.exists(backup_dir) and not eval(args.is_remote_client if args.is_remote_client else 'False'):
            os.makedirs(backup_dir)
            
        if args.is_remote_client and eval(args.is_remote_client):
            temp_backup_dir = args.temp_bkp_path
            vals.update(backup_dir=temp_backup_dir)
                
        backup_store_res = self.store_backup_file(args, vals)
        if backup_store_res and not backup_store_res.get('status'):
            raise Exception(backup_store_res.get('message'))

        self.filename = backup_store_res.get('filename')
        self.backup_time = backup_store_res.get('backup_time')
        self.backup_file_path = backup_store_res.get('backup_file_path')
        
        if args.is_remote_client and eval(args.is_remote_client):
            self.backup_file_path = os.path.join(backup_dir, self.filename)
            self.temp_bkp_file_path = backup_store_res.get('backup_file_path')
            response = self._create_saas_remote_backup(args)
            
        return response
    
    def _create_remote_backup(self, args, vals):
        """
            Method to create the temporary database backup on main server and store it on the remote server.
            The temporary DB Backup file will be deleted after storing it on the remote server. 
        """
        response = dict(status=False)
        backup_dir = vals.get('backup_dir')
        temp_backup_dir = args.temp_bkp_path
        vals.update(backup_dir=temp_backup_dir)
        check_path_res = self.check_remote_backup_path(args, backup_dir)
        if check_path_res and not check_path_res.get('status'):
            raise Exception(check_path_res.get('message'))
        backup_store_res = self.store_backup_file(args, vals)
        if backup_store_res and not backup_store_res.get('status'):
            raise Exception(backup_store_res.get('message'))

        self.filename = backup_store_res.get('filename')
        self.backup_time = backup_store_res.get('backup_time')
        self.temp_backup_file_path = backup_store_res.get('backup_file_path')
        self.remote_backup_file_path = os.path.join(backup_dir, self.filename)
        self.backup_file_path = self.remote_backup_file_path
        
        sftp = self.ssh_obj.open_sftp()
        sftp.put(self.temp_backup_file_path, self.remote_backup_file_path)
        sftp.close()
        
        cmd = f"ls -f {self.remote_backup_file_path}"

        # Checking if the backup file is successfully copied to remote server
        check_file_exist = self.execute_on_remote_shell(self.ssh_obj,cmd)
        if check_file_exist and check_file_exist.get("status"):
            print("\nBackup file successfully copied to the remote server.")
            print("remote backup_file_path --->", self.remote_backup_file_path)
            
            # DELETE the temporary backup file from the Main Server
            if os.path.exists(self.temp_backup_file_path):
                os.remove(self.temp_backup_file_path)
                print("\nBackup file successfully deleted from the Main Server.")
            
            response.update(status=True)
            return response
        else:
            print("\nBackup file doesn't successfully moved to the remote server.")
            raise Exception("Backup file couldn't be moved to remote server.")
        

    
    def login_saas_remote(self, remote):
        """
            Method to login to the remote SaaS server using SSH.
        """
        try:
            ssh_obj = paramiko.SSHClient()
            ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_obj.connect(hostname=remote.get('host'), username=remote.get('user'), password=remote.get('password'),port=remote.get('port'))
            self.saas_ssh_obj = ssh_obj
        except Exception as e:
            print("Couldn't connect remote SaaS server: ", e)
            raise Exception("Couldn't connect to remote SaaS server.")
    
    
    def _create_saas_remote_backup(self, args):
        """
            This method is crated to make the compatibility with SaaS Kit Backup module.
            This method will copy the local backup file to the remote saas server.
            The temporary backup file will be deleted after storing it on the remote saas server.
        """
        saas_url = 'http://localhost:8069/remote/server/creds'
        saas_data = {
            'backup_process_id': int(args.processid)
        }
        response = dict(status=False)
        try:
            # Getting the host server creds of the remote saas server
            with requests.post(saas_url, data=saas_data, stream=True) as saas_response:
                saas_response.raise_for_status()
                resp = json.loads((saas_response.content).decode())
                
                # Uploading the backup file from the main server to remote saas server
                self.login_saas_remote(resp.get('host_server'))
                if self.saas_ssh_obj:
                    saas_sftp = self.saas_ssh_obj.open_sftp()
                    saas_sftp.put(self.temp_bkp_file_path, self.backup_file_path)

                    # Removing the temporary backup on the main server 
                    if os.path.exists(self.temp_bkp_file_path):
                        saas_sftp.remove(self.temp_bkp_file_path)
                    saas_sftp.close()
                    print("Local Backup File Successfully Copied to the Remote SaaS Server")

            response.update(status=True)
        except Exception as e:
            print("Exception while copying the local backup to the remote saas server")
            raise Exception("Local Backup file couldn't be moved to remote saas server.")
            
        return response



if __name__ == '__main__':
    backup_storage = BackupStorage()
    parser = backup_storage.init_parser()
    args = parser.parse_args()
    print(backup_storage.manage_backup_files(args))


