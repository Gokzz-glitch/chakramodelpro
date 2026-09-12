$Url = "https://datasets.simula.no/downloads/kvasir-seg.zip"
$ZipFile = "data\raw\kvasir-seg.zip"
$ExtractPath = "data\raw"

Write-Host "Creating directories..."
New-Item -ItemType Directory -Force -Path "data\raw" | Out-Null

Write-Host "Downloading Kvasir-SEG dataset from $Url ..."
Invoke-WebRequest -Uri $Url -OutFile $ZipFile

Write-Host "Extracting dataset..."
Expand-Archive -Path $ZipFile -DestinationPath $ExtractPath -Force

Write-Host "Cleaning up zip file..."
Remove-Item -Path $ZipFile -Force

Write-Host "Kvasir-SEG dataset downloaded and extracted successfully."
