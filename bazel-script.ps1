$path = $args[0]
$name = $args[1]
$delete = $args[2]
$iterations = $args[3]
$script_home = Get-Location
$process = 0
cd $path

for ($i = 0; $i -lt $iterations; $i++ ) {
	if($delete -ne "false") {
		rm -r -Force .\bazel-bin\*
		rm -r -Force .\bazel-out\*
		rm -r -Force .\bazel-$delete\*
	}
    $bazel_id = (Start-Process bazel -ArgumentList "build //:everything_deploy.jar" -passthru).ID
    sleep(1)
	echo bazel id":" $bazel_id
    $process=(ps | grep java| tr -s ' ' | cut -d ' ' -f 7)
	echo process ids":" $process
    python $script_home\logPID-bazel.py $bazel_id $process
    sleep(2)
    Rename-Item -Path .\log.txt -NewName $name-bazel-performance-log-$i.txt
    Rename-Item -Path .\img.png -NewName $name-bazel-performance-$i.png
    mv .\$name-bazel-performance-log-$i.txt -Destination $script_home\results
    mv .\$name-bazel-performance-$i.png -Destination $script_home\results
} 

bazel query 'deps(//:everything)' --notool_deps --noimplicit_deps --output graph > graph.in
Get-Content -Path "graph.in" | Out-File -FilePath "newgraph.in" -Encoding ascii
rm graph.in
dot "-Tpng" "newgraph.in" -o "$name-bazel-dependencies.png"
rm newgraph.in
mv .\$name-bazel-dependencies.png -Destination $script_home\results
cd $script_home