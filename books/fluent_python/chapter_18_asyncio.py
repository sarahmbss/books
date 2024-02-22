'''
    Concurrency vs Parallelism
        - Concurrency is about dealing with lots of things at once.
        - Parallelism is about doing lots of things at once.
        - Not the same, but related.
        - One is about structure, one is about execution.
        - Concurrency provides a way to structure a solution to solve a problem that may (but not
        necessarily) be parallelizable
        - For real parallelism, you must have multiple cores

    Asyncio
        - package that implements concurrency with coroutines driven by an event loop
'''