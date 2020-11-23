# swevolutioncalculator

## TO USE
1. Build Add, Subtract, Multiply, and Divide using maven.
2. Install each of the above to local maven repository
3. Run Calculator

## Maven
You need to configure the pom.xml with the maven dependency plugin and the maven jar plugin so that the dependencies are all packaged into one jar and so that the classpath is defined.

## Gradle
We copied the Maven Calculator project and ran gradle init. This did not pick up any of the plugins applied previously to apply dependency packaging and classpath definitions, so this had to be done manually. We then applied the shadow plugin and had to run gradle shadow to generate a jar that included all dependencies and would run.
