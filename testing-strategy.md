# Testing Strategy

## Coverage Strategy

As our program is quite simple and a large portion of our code is contained within helper methods with few decision points or branches, we decided that the most effective coverage strategy would be **statement coverage**.

## Identifying Test Cases

### Helper Methods

To identify test cases for static **helper methods** that _do not reach out to an external network_, we simply examined the source code and created a single unit test for each of these methods. By testing these statements alone, we were able to reach 41% statement coverage.

To ensure that our test cases were useful, we first made a call to the OpenWeather API and saved the JSON response payload as a **stub** - `stubResponse.json`. We are then able to use this stubbed data to assert that the methods were behaving correctly with real data, and returning appropriate responses.
