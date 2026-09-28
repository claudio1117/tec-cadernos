param(
    [switch]$ListPages,
    [string]$DebugUrl = 'http://127.0.0.1:9222',
    [string]$WebSocketUrl
)

$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
try {
    if ($ListPages) {
        $pages = Invoke-RestMethod -Uri "$DebugUrl/json" -TimeoutSec 5
        [Console]::WriteLine((ConvertTo-Json -InputObject @($pages) -Depth 10 -Compress))
        exit 0
    }
    $ws = New-Object System.Net.WebSockets.ClientWebSocket
    $ws.Options.SetRequestHeader('Origin', $DebugUrl)
    $cancel = New-Object System.Threading.CancellationTokenSource
    $cancel.CancelAfter(10000)
    $null = $ws.ConnectAsync([Uri]$WebSocketUrl, $cancel.Token).GetAwaiter().GetResult()
    while ($null -ne ($line = [Console]::ReadLine())) {
        $request = $line | ConvertFrom-Json
        $cancel.Dispose()
        $cancel = New-Object System.Threading.CancellationTokenSource
        $cancel.CancelAfter(60000)
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($line)
        $segment = New-Object 'System.ArraySegment[byte]' -ArgumentList (,$bytes)
        $null = $ws.SendAsync($segment, [System.Net.WebSockets.WebSocketMessageType]::Text,
            $true, $cancel.Token).GetAwaiter().GetResult()
        do {
            $stream = New-Object System.IO.MemoryStream
            do {
                $buffer = New-Object byte[] 65536
                $segment = New-Object 'System.ArraySegment[byte]' -ArgumentList (,$buffer)
                $received = $ws.ReceiveAsync($segment, $cancel.Token).GetAwaiter().GetResult()
                if ($received.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
                    throw 'O Chrome encerrou a conexão'
                }
                $stream.Write($buffer, 0, $received.Count)
            } while (-not $received.EndOfMessage)
            $response = [System.Text.Encoding]::UTF8.GetString($stream.ToArray())
            $stream.Dispose()
            $message = $response | ConvertFrom-Json
        } while ($message.id -ne $request.id)
        [Console]::WriteLine($response)
    }
    $ws.Dispose()
    $cancel.Dispose()
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
