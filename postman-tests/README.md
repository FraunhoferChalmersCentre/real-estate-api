# Generate Postman server tests

When developing a server that implements an OpenAPI Specification (OAS) it is helpful to have simple tests that verify some basic functionality.
By using a tool called [portman](https://github.com/apideck-libraries/portman), we can atuomatically create such tests from the OAS.
These tests can be imported into [Postman](https://www.postman.com/).

For each GET path in the OAS, the following tests are generated:
* Verify that the server responds with a 2xx [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#successful_responses) (also created for POST requests)
* Verify that the expected content header is set (usually `application/json`)
* If JSON is expected in the response:
  - Verify that the body has valid JSON
  - Verify that the body adheres to the specified JSON-schema

For convenience, the procedure and the required dependencies are bundled in a Docker image.

## Example

We provide two simple shell scripts that builds the image and runs the container respectively.

Build:
```
$ ./build_image.sh
```

Generate the Postman test collection:
```
$ ./create_postman_tests.sh
```
As long as the image is already built, you can run this script anytime you change the API to generate new tests. Afterwards, you should see a JSON file in the current directory:
```
$ ls -l | grep *.json
-rw-r--r-- 1 adrian adrian 93013 Sep  7 10:17 postman_tests.json
```
You can import this file into Postman.

## Windows users
On Windows, you have two alternatives.

### Use a Unix environment
The [example](#example) should work as-is if executed in a Unix environment such as Git Bash or Windows Subsystem for Linux (WSL).

### Build manually

If you choose to work in PowerShell, you can build the container with:
```
PS real-estate-api> docker build -f .\postman-tests\Dockerfile.oas-to-postman -t fcc-sys/oas-to-postman .
```
Note that you should be in the `real-estate-api` directory to send the appropriate build context.

To run the container, use the PowerShell script:
```
PS postman-tests> .\create_postman_tests.ps1
```
