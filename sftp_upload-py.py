 ```

     import paramiko,logging,threading,sys
      
      def sftp_operation(local_file_path, local_file_name, sftp_host,
                     sftp_port, sftp_user, sftp_password, private_key_location,
                     private_key_password, remote_folder):
      """
          Performs an SFTP operation to upload a file to a remote server.
      
          Parameters:
                      @param: local_file_path (str): The path of the file on the local system.
                      @param: local_file_name (str): The name of the file on the local system.
                      @param: sftp_host (str): The hostname of the SFTP server.
                      @param: sftp_port (int): The port number of the SFTP server.
                      @param: sftp_user (str): The username to authenticate with the SFTP server.
                      @param: sftp_password (str): The password to authenticate with the SFTP server.
                      @param: private_key_location (str): The location of the private key file for authentication.
                      @param: private_key_password (str): The password of the private key file.
                      @param: remote_folder (str): The directory on the SFTP server where the file will be uploaded.
      """
      
      # Set up logging
      log_file_location = r"[Path_to_log_files]" #copmlete your values
      log_file_name = f"[File name prefix]]-{threading.get_ident()}.log" ##copmlete your values
      logging.basicConfig(filename=f"{log_file_location}\\{log_file_name}", level=logging.DEBUG,
                          format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
      
      # Create a new SSH client
      ssh = paramiko.SSHClient()
      logging.info("ssh opened sshClient()")
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      try:
          # Connect to the server
          private_key = paramiko.RSAKey.from_private_key_file(private_key_location, password=private_key_password)
          logging.info("private key set")
          ssh.connect(sftp_host, port=sftp_port, username=sftp_user, password=sftp_password, pkey=private_key
                      ,gss_deleg_creds=True)
          logging.info('Connectong with\n'+f"{sftp_host}\n{sftp_port}\n{sftp_user}\n{sftp_password}\nPrivate key\ngss_deleg_creds=True")
          #ssh.connect(sftp_host, port=sftp_port, username=sftp_user, password=sftp_password)
          #ssh.connect(sftp_host, port=sftp_port, username=sftp_user, pkey=private_key)
          logging.debug("Connected to the server")
      
          # Create a new SFTP session
          sftp = ssh.open_sftp()
          logging.debug("SFTP session opened")
      
          # Upload the file
          sftp.put(local_file_path, f"{remote_folder}/{local_file_name}",confirm=True)
          logging.debug(f"File '{local_file_name}' uploaded")
      
          # List the contents of the remote directory
          logging.debug("Contents of the remote directory:")
          for file in sftp.listdir(remote_folder):
              logging.debug(file)
      
          # Close the SFTP session
          sftp.close()
          logging.debug("SFTP session closed")
      
      except Exception as e:
          logging.error(f"An error occurred: {e}")
      
      finally:
          # Close the SSH client
          ssh.close()
          logging.debug("Server connection closed")
      if __name__ == "__main__":
      sftp_operation(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])'