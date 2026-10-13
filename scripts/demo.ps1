param([int]$Start=0, [string]$PreviousHash='', [string]$CliPath='../intent-firewall/node_modules/genlayer/dist/index.js', [string]$Account='studio-proof-deployer')
$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$deployment=Get-Content deployment.json -Raw | ConvertFrom-Json
$cli=$CliPath
if(-not (Test-Path $cli)){throw 'Install GenLayer CLI 0.39.2 and pass -CliPath pointing to genlayer/dist/index.js.'}
$env:ADVISORY_FUSE_ACCOUNT=$Account
$env:STUDIO_NATIVE_BROADCAST='1'
function Check-Receipt([string]$Hash,[string]$Mode='--success'){
    $arguments=@('scripts/check.mjs',$Mode,$Hash)
    if($Mode -eq '--error'){$arguments+='closed or stale trial'}
    $output=& node @arguments
    if($LASTEXITCODE -ne 0){throw "Receipt not verified for $Hash. Do not rebroadcast; inspect status first."}
    $output
}
function Inspect-State{
    $output=& node scripts/inspect.mjs $deployment.contract $deployment.creator $deployment.demo_name
    if($LASTEXITCODE -ne 0){throw 'State/root inspection failed. No further writes.'}
    return ($output | ConvertFrom-Json)
}
function Send-Step([int]$Trial){
    # Capture all CLI output privately; never print RPC validator configurations.
    # Windows PowerShell 5 wraps redirected native stderr as ErrorRecord.
    # Capture it without allowing the public BROADCAST_HASH stderr line to abort parsing.
    $savedPreference=$ErrorActionPreference
    try{
        $ErrorActionPreference='Continue'
        $output=& node --require ./scripts/pin_cli_context.cjs --require ./scripts/broadcast_once.cjs $cli write $deployment.contract step --args $deployment.experiment_key $Trial 2>&1
    }finally{$ErrorActionPreference=$savedPreference}
    $hashes=@($output | ForEach-Object {if($_.ToString() -match '^BROADCAST_HASH (0x[0-9a-fA-F]{64})$'){$Matches[1]}} | Select-Object -Unique)
    if($hashes.Count -ne 1){throw 'No unique broadcast hash. Outcome may be unknown: inspect wallet history before rerunning.'}
    $hash=$hashes[0]
    Write-Host ("BROADCAST_HASH "+$hash)
    return $hash
}
if($Start -lt 0 -or $Start -gt 5){throw 'Start must be 0..5'}
if($Start -gt 0 -and $PreviousHash -notmatch '^0x[0-9a-fA-F]{64}$'){throw 'PreviousHash required when resuming'}
if($PreviousHash){Check-Receipt $PreviousHash}
else{Check-Receipt $deployment.verified_receipts.activation}
& node scripts/check.mjs --source $deployment.contract
if($LASTEXITCODE -ne 0){throw 'Source mismatch or failed source read'}
for($trial=$Start;$trial -lt 6;$trial++){
    $before=Inspect-State
    if($before.state -ne 'ACTIVE' -or $before.trials -ne $trial -or $null -eq $before.next){throw 'Unexpected/expired pre-state. Do not replay a consumed trial.'}
    $hash=Send-Step $trial
    Check-Receipt $hash
    $after=Inspect-State
    if($after.trials -ne ($trial+1)){throw 'Trial did not advance exactly once'}
    @{trial=$trial;hash=$hash;state=$after.state;stats=$after.stats;next=$after.next;observation=$after.reports[-1]} | ConvertTo-Json -Depth 8 -Compress
}
# Deliberate replay is an expected ERROR, never counted as successful execution.
$hash=Send-Step 0
Check-Receipt $hash '--error'
$final=Inspect-State
if($final.state -ne 'COMPLETE' -or $final.trials -ne 6){throw 'Replay changed terminal state'}
@{replay=$hash;state=$final.state;trials=$final.trials;roots_verified=$final.roots_verified} | ConvertTo-Json -Compress
