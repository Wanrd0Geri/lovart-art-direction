param(
    [string]$Route,
    [string]$Prompt,
    [switch]$RouteOnly,
    [switch]$Regressions
)

$ErrorActionPreference = 'Stop'
$scriptRoot = $PSScriptRoot
$userProfilePath = $env:USERPROFILE
if ([string]::IsNullOrWhiteSpace($userProfilePath)) {
    $userProfilePath = [Environment]::GetFolderPath('UserProfile')
}
$bundledPython = Join-Path $userProfilePath '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

function Resolve-TaskPython {
    if (Test-Path -LiteralPath $bundledPython) {
        return $bundledPython
    }

    foreach ($commandName in @('python3', 'python')) {
        $command = Get-Command $commandName -ErrorAction SilentlyContinue
        if ($null -ne $command) {
            try {
                & $command.Source --version *> $null
                if ($LASTEXITCODE -eq 0) {
                    return $command.Source
                }
            }
            catch {
                continue
            }
        }
    }

    throw 'No usable Python runtime found. The Codex bundled runtime and system python3/python were checked.'
}

$taskPython = Resolve-TaskPython
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

if ($Regressions) {
    & $taskPython (Join-Path $scriptRoot 'run_regressions.py')
    exit $LASTEXITCODE
}

if ([string]::IsNullOrWhiteSpace($Route)) {
    throw '-Route is required unless -Regressions is used.'
}

$resolvedRoute = [System.IO.Path]::GetFullPath($Route)
if (-not (Test-Path -LiteralPath $resolvedRoute -PathType Leaf)) {
    throw "Route manifest not found: $resolvedRoute"
}

& $taskPython (Join-Path $scriptRoot 'validate_route.py') $resolvedRoute
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if ($RouteOnly) {
    exit 0
}

if ([string]::IsNullOrWhiteSpace($Prompt)) {
    throw '-Prompt is required unless -RouteOnly is used.'
}

$resolvedPrompt = [System.IO.Path]::GetFullPath($Prompt)
if (-not (Test-Path -LiteralPath $resolvedPrompt -PathType Leaf)) {
    throw "Compiled prompt not found: $resolvedPrompt"
}

& $taskPython (Join-Path $scriptRoot 'lint_prompt.py') --route $resolvedRoute --prompt $resolvedPrompt
exit $LASTEXITCODE
