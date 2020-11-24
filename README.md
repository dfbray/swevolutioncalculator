# swevolutioncalculator

## TO USE
1. Build Add, Subtract, Multiply, and Divide using maven.
2. Install each of the above to local maven repository
3. Run Calculator

## Maven
You need to configure the pom.xml with the maven dependency plugin and the maven jar plugin so that the dependencies are all packaged into one jar and so that the classpath is defined.

## Gradle
We copied the Maven Calculator project and ran gradle init. This did not pick up any of the plugins applied previously to apply dependency packaging and classpath definitions, so this had to be done manually. We then applied the shadow plugin and had to run gradle shadow to generate a jar that included all dependencies and would run.

## Bazel
After much effort, we decided to host the local maven repository by navigating to ~mvn-home\.m2\repository and executing python -m http.server 8000. This allowed us to specify localhost:8000 in the WORKSPACE file for downloading maven artifacts. We then had to modify the BUILD file to add the main_class attribute as well as restrucutre to support the java_binary goal. We then had to execute bazel build //:Calculator_deploy.jar . Emphasis on the underscore deploy, which generates the jarfile with all dependencies included.
