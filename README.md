# reading-insights

# Why

Wanted to see if I can figure out the logic behind what makes a sentence gets quoted / highlighted a lot.

# How

Collect quotes from Goodreads (inc. relevant attributes).

# What

Three crawlers:
1. `goodreads.quotes.popular`

Starts from https://www.goodreads.com/quotes?page=1

Collects the first-level Popular quotes, follows paginations.

2. `goodreads.quotes.by_category`

Starts from https://www.goodreads.com/quotes?page=1

Traverses the categories, collects Popular quotes for that category, follows pagination.

3. `goodreads.quotes.book`

Not implemented yet. The idea is to collect all the quotes for a particular book. TODO: accept the book URL as spider arg.

