$path = $args[0]
$name = $args[1]
$iterations = $args[2]
$script_home = Get-Location
$process = 0
cd $path

for ($i = 0; $i -lt $iterations; $i++ ) {
    rm -r -Force .\build
    $gradle_id = (Start-Process gradle -ArgumentList "build -x test" -passthru).ID
    sleep(0.5)
	echo gradle id":" $gradle_id
    $process=(ps | grep java| tr -s ' ' | cut -d ' ' -f 7)
	echo process ids":" $process
    python $script_home\logPID-gradle.py $gradle_id $process
    sleep(2)
    Rename-Item -Path .\log.txt -NewName $name-gradle-performance-log-$i.txt
    Rename-Item -Path .\img.png -NewName $name-gradle-performance-$i.png
    mv .\$name-gradle-performance-log-$i.txt -Destination $script_home\results
    mv .\$name-gradle-performance-$i.png -Destination $script_home\results
} 

gradle generateDependencyGraph
Rename-Item -Path .\build\reports\dependency-graph\dependency-graph.png -NewName $name-gradle-dependencies.png
mv .\build\reports\dependency-graph\$name-gradle-dependencies.png -Destination $script_home\results
cd $script_home