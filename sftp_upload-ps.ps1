# Load WinSCP .NET assembly
Add-Type -Path "C:\Program Files (x86)\WinSCP\WinSCPnet.dll"

# Setup session options
$sessionOptions = New-Object WinSCP.SessionOptions -Property @{
    Protocol = [WinSCP.Protocol]::Sftp
    HostName = "host_name"
    UserName = "hardcoded_username"
    Password = "hardcoded-password"
    PortNumber = hardcoded_port_number
    SshPrivateKeyPath = "path_to_private_key"
    GiveUpSecurityAndAcceptAnySshHostKey = $true
    SshPrivateKeyPassphrase = "privateKey_passphrase"
}

$session = New-Object WinSCP.Session

try {
    # Connect
    $session.Open($sessionOptions)

    # Define transfer options
    $transferOptions = New-Object WinSCP.TransferOptions
    $transferOptions.TransferMode = [WinSCP.TransferMode]::Binary

    # Upload file to the /1 Ilya directory
    $transferResult = $session.PutFiles("local file path", "remote_folder_path", $False, $transferOptions)

    # Throw on any error
    $transferResult.Check()

    # Print results
    foreach ($transfer in $transferResult.Transfers) {
        Write-Host ("Upload of {0} succeeded" -f $transfer.FileName)
    }

    # List the files in /1 Ilya directory
    $directoryInfo = $session.ListDirectory("remote_folder_patha")

    Write-Host "Listing files in remote_folder_path directory:"
    foreach ($fileInfo in $directoryInfo.Files) {
        Write-Host $fileInfo.Name
    }
}
finally {
    # Disconnect, clean up
    $session.Dispose()
}
