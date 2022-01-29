## Your Challenge

The attached data contains records of our users' activities and associated metadata.
Using the provided data set, calculate for a given user the number of times the following rules have been satisfied:

-   They ran more than 1km in a single run, 3 days in a row. This should count once per 3 consecutive days. i.e.: having at least one 1k run 6 days in a row counts as 2-times, not 4-times.
-   They ran more than 10km in a calendar week. Consider a calendar week as starting on Monday and ending on Sunday.
-   Be creative and make up a 3rd rule based on what you see in the data.

Your program should accept a single user id as input (either as a command line argument or from stdin), and output JSON to stdout. Feel free to make assumptions about these requirements and document them as part of your submission.

### Notes on the data set

-   All of this data is derived from real data from our system
-   IDs have been anonymized
-   Units:
    -   distance: kilometers
    -   speed: km/h
    -   pace: minute/km
    -   ascent/descent: meters

## Expectations

Use the language and framework that you are most comfortable using. Don't spend more than a few hours on this. Writing code iterably is important, so we expect to see shortcuts, assumptions, and simple mistakes. Since much of software engineering is about making trade-offs, please be prepared to discuss the benefits and shortcomings of your submission.

Your submission must work! Please provide sample executions and clear instructions on how to run your program and interpret its output. We use MacOS and generally have homebrew and JVMs available. If that environment isn't available to you, that's fine! We'll do our best!

## Discussion

If you've submitted a satisfactory program (it fulfills the challenge, it's comprehensible, and there are no major defects), we'll invite you to an in person interview where we'll review your submission together. Don't worry, we're not going to pick through it looking for gotchas. We want to gauge your ability to be successful within our environment by using your code as a prop for discussion to learn about you as much as possible during the short hours that you're here. Please refer to the attached job description for more details about our environment.

During the discussion we may want to add further requirements to a system based on your code. Your program may or may not be able to support those requirements, so be prepared to discuss different approaches to the problem and solution.

You should be prepared to discuss:

-   The design of your code
-   The algorithms and data structures you used
-   The assumptions and trade-offs you made
-   How you tested it
-   Ideas for future improvements

Some points that are of particular interesting to us are:

-   How will it scale?
-   How would this work in a distributed fashion?
-   Would it store data? How?
-   How would this interface with other systems and clients?
