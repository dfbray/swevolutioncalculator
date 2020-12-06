$path = $args[0]
$name = $args[1]
$iterations = $args[2]
$script_home = Get-Location
cd $path


for ($i = 0; $i -lt $iterations; $i++ ) {
    rm -r -Force .\target
    Start-Process mvn -ArgumentList "package -DskipTests"
    sleep(1)
    $process=(ps | grep java| tr -s ' ' | cut -d ' ' -f 7)
    python $script_home\logPID-maven.py $process
    Rename-Item -Path .\log.txt -NewName $name-maven-performance-log-$i.txt
    Rename-Item -Path .\img.png -NewName $name-maven-performance-$i.png
    mv .\$name-maven-performance-log-$i.txt -Destination $script_home\results
    mv .\$name-maven-performance-$i.png -Destination $script_home\results
} 

mvn depgraph:graph
cd target
dot -Tpng dependency-graph.dot -o $name-maven-dependencies.png
mv $name-maven-dependencies.png -Destination $script_home\results
cd $script_home