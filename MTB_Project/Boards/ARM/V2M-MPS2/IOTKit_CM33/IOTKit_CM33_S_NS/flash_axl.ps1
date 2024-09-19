
#  check if there is a device mounted with the name V2M_MPS2
$device = Get-CimInstance -ClassName Win32_Volume | Where-Object { $_.Label -eq 'V2M_MPS2' }

if ($device -eq $null) {
    Write-Host "No device mounted with the name V2M_MPS2"
    exit
}
else {
    # check the device path
    $devicePath = $device.DriveLetter + "\"
    Write-Host "Device mounted with the name V2M_MPS2 in path: $devicePath"
}

# declare variables with path name
$NonSecureAxf = "IOTKit_CM33_ns.axf"
$SecureAxf = "IOTKit_CM33_s.axf"

# declare variables with path name
$flashNonSecureAxf = ".\IOTKit_CM33_ns\Objects\" + $NonSecureAxf
$flashSecureAxf = ".\IOTKit_CM33_s\Objects\" + $SecureAxf

$flashNonSecureAxfDestiny = $devicePath + '\\SOFTWARE\\' + $NonSecureAxf
$flashSecureAxfDestiny = $devicePath + '\\SOFTWARE\\' + $SecureAxf


$imageFile = "images.txt"
$imageDevicePath = $devicePath + "\MB\HBI0263C\AN505\" + $imageFile

# check if the files exist
if (-not (Test-Path "$flashNonSecureAxf")) {
    Write-Host "File $flashNonSecureAxf not found in the device"
    exit
}

if (-not (Test-Path "$flashSecureAxf")) {
    Write-Host "File $flashSecureAxf not found in the device"
    exit
}

# check if the image file exists
if (-not (Test-Path "$imageFile")) {
    Write-Host "File $imageFile not found in the device"
    exit
}

# copy the files to the device
Copy-Item -Path $flashNonSecureAxf -Destination $flashNonSecureAxfDestiny
Copy-Item -Path $flashSecureAxf -Destination $flashSecureAxfDestiny
Copy-Item -Path $imageFile -Destination $imageDevicePath

# check if the files were copied
if (-not (Test-Path "$flashNonSecureAxfDestiny")) {
    Write-Host "File $flashNonSecureAxf not copied to the device"
    exit
}

if (-not (Test-Path "$flashSecureAxfDestiny")) {
    Write-Host "File $flashSecureAxf not copied to the device"
    exit
}

if (-not (Test-Path "$imageDevicePath")) {
    Write-Host "File $imageFile not copied to the device"
    exit
}