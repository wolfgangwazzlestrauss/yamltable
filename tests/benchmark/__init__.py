"""Benchmark tests for the yamltable library."""


import pytest_benchmark.fixture as bm

import yamltable


def benchmark_dependencies(benchmark: bm.BenchmarkFixture) -> None:
    """Benchmark dependency resolution sorting."""

    dicts = [
        {"name": 1, "depends": [2]},
        {"name": 2, "depends": []},
    ]

    benchmark(yamltable.dependencies, dicts, "depends", "name")
