# Symbol data point tracker

## Building & running

To build & start the service run:
```commandline
docker-compose up -d
```

The API docs will be available at:
http://localhost:8000/docs

Running tests:
```commandline
docker-compose exec web pytest .
```

Postman collection for manual testing:
[tracker.postman_collection.json](tracker.postman_collection.json)

## Solution

To ensure O(1) time complexity for calculating the stats, for each new batch added:
- the rolling average is updated
- rolling sum of squares is updated for variance calculation
- two deques are updated using the [sliding window min/max algorithm](https://www.nayuki.io/page/sliding-window-minimum-maximum-algorithm) to keep track of min & max values

Variance formula used:
$$
\text{Var}(X) = E(X^2) - [E(X)]^2
$$

The approach was to:
1. Build a simple O(n) solution in TDD first
2. Generate 10^6 random points and insert using the /add_batch API
3. Add tests for windows from 10 to 10^6
4. Replace the O(n) implementation with O(1)

## Assumptions

1. If the window is larger than the current number of values — calculate the stats instead of throwing errors.  
   This was done to simplify testing on a small number of values. 

2. The data source for the data points ensures there are no negative values.  
   The algorithm would still work, but considering we're dealing with trading prices, negative numbers shouldn't be expected.  
   Adding a validator for negative numbers would require either an additional iteration over the whole batch,  
   or the check would have to be performed when iterating over values to calculate the stats. 
