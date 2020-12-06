$path = $args[0]
$name = $args[1]
$iterations = $args[2]
$script_home = Get-Location
$process = 0
$bad_process = 0
cd $path

for ($i = 0; $i -lt $iterations; $i++ ) {
    rm -r -Force .\build
    Start-Process gradle -ArgumentList "build -x test"
    sleep(1)
    $process=(ps | grep java| tr -s ' ' | cut -d ' ' -f 7)

    $processes = [System.Collections.ArrayList]$process

    if($processes -contains $bad_process) {
	 $processes.Remove($bad_process)
    }

    $process = $processes[0]
    python $script_home\logPID-gradle.py $process $bad_process

    if($LastExitCode -ne 0) {
        $bad_process = $LastExitCode
    }

    sleep(1)
    Rename-Item -Path .\log.txt -NewName $name-gradle-performance-log-$i.txt
    Rename-Item -Path .\img.png -NewName $name-gradle-performance-$i.png
    mv .\$name-gradle-performance-log-$i.txt -Destination $script_home\results
    mv .\$name-gradle-performance-$i.png -Destination $script_home\results
} 

gradle generateDependencyGraph
Rename-Item -Path .\build\reports\dependency-graph\dependency-graph.png -NewName $name-gradle-dependencies-$i.png
mv .\build\reports\dependency-graph\$name-gradle-dependencies-$i.png -Destination $script_home\results
cd $script_home