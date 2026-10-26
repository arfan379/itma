"""
Tests for ITMA Sample GTFS Generator (tests/test_sample_gtfs.py)
Validates that the CI GTFS ZIP is structurally valid and contains
expected files, routes, and midnight-crossing stop times.
"""

import os
import csv
import zipfile
import tempfile
import pytest

from src.ingestion.sample_gtfs import generate_sample_gtfs_zip


@pytest.fixture
def sample_zip_path():
    """Generate a sample GTFS ZIP in a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test_gtfs.zip")
        generate_sample_gtfs_zip(output_path=path)
        yield path


def test_zip_contains_required_files(sample_zip_path):
    """GTFS ZIP must contain routes, stops, trips, stop_times, feed_info."""
    required_files = {
        "routes.txt", "stops.txt", "trips.txt",
        "stop_times.txt", "feed_info.txt"
    }
    with zipfile.ZipFile(sample_zip_path, "r") as zf:
        names = set(zf.namelist())
    assert required_files.issubset(names), (
        f"Missing: {required_files - names}"
    )


def test_routes_have_expected_ids(sample_zip_path):
    """routes.txt must include at least TJ-1, TJ-2, TJ-3."""
    with zipfile.ZipFile(sample_zip_path, "r") as zf:
        with zf.open("routes.txt") as f:
            reader = csv.DictReader(
                line.decode("utf-8") for line in f
            )
            route_ids = {row["route_id"] for row in reader}

    assert {"TJ-1", "TJ-2", "TJ-3"}.issubset(route_ids)


def test_stop_times_contain_midnight_crossing(sample_zip_path):
    """stop_times.txt must have at least one time >= 24:00:00."""
    with zipfile.ZipFile(sample_zip_path, "r") as zf:
        with zf.open("stop_times.txt") as f:
            reader = csv.DictReader(
                line.decode("utf-8") for line in f
            )
            has_midnight = any(
                int(row["arrival_time"].split(":")[0]) >= 24
                for row in reader
            )
    assert has_midnight, "Expected at least one arrival_time >= 24:00:00"
