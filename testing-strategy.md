# Testing Strategy

## Coverage Strategy

As our program is quite simple and a large portion of our code is contained within helper methods with few decision points or branches, we decided that the most effective coverage strategy would be **statement coverage**.

## Identifying Test Cases

We chose to pick test cases via statement testing. In order to do this, we create our main tests based on coverage.

### Helper Methods

To identify test cases for static **helper methods** that _do not reach out to an external network_, we simply examined the source code and created a single unit test for each of these methods. By testing these statements alone, we were able to reach 41% statement coverage.
We make each one it's own test case, in order to make sure each one functions appropriately should there be an error.

## Mocks
To ensure that our test cases were useful, we first made a call to the OpenWeather API and saved the JSON response payload as a **stub** - `stubResponse.json`. We are then able to use this stubbed data to assert that the methods were behaving correctly with real data, and returning appropriate responses.

This is done by mocking the request function to instead return the json file from the file instead of calling the API, via the Mock Patch.

With this, we are able to call the file using the CliRunner function, and request from the stub.

With this, we can test the main logic and the infeasable cases.

These cases include help with other arguements, which just calls help, no info selected, too many locations, and no api.

Our tests for checking multiple arguements will check every arguement to ensure maximum coverage.