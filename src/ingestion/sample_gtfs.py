"""
ITMA - Sample GTFS Generator (sample_gtfs.py)
Creates a minimal, self-contained GTFS ZIP feed for CI/CD testing.
This avoids dependency on external GTFS downloads during CI runs.
"""

import csv
import io
import os
import zipfile

# TransJakarta-inspired sample data
ROUTES = [
    {"route_id": "TJ-1", "agency_id": "TJ", "route_short_name": "1",
     "route_long_name": "Blok M - Kota", "route_type": "3"},
    {"route_id": "TJ-2", "agency_id": "TJ", "route_short_name": "2",
     "route_long_name": "Pulogadung - Harmoni", "route_type": "3"},
    {"route_id": "TJ-3", "agency_id": "TJ", "route_short_name": "3",
     "route_long_name": "Kalideres - Pasar Baru", "route_type": "3"},
]

STOPS = [
    {"stop_id": "BM", "stop_name": "Blok M",
     "stop_lat": "-6.2444", "stop_lon": "106.7981"},
    {"stop_id": "MH", "stop_name": "Masjid Hidayatullah",
     "stop_lat": "-6.2350", "stop_lon": "106.7978"},
    {"stop_id": "BD", "stop_name": "Bendungan Hilir",
     "stop_lat": "-6.2150", "stop_lon": "106.8100"},
    {"stop_id": "KT", "stop_name": "Kota",
     "stop_lat": "-6.1375", "stop_lon": "106.8175"},
    {"stop_id": "PG", "stop_name": "Pulogadung",
     "stop_lat": "-6.1900", "stop_lon": "106.8900"},
    {"stop_id": "HM", "stop_name": "Harmoni",
     "stop_lat": "-6.1666", "stop_lon": "106.8233"},
    {"stop_id": "KD", "stop_name": "Kalideres",
     "stop_lat": "-6.1588", "stop_lon": "106.7030"},
    {"stop_id": "PB", "stop_name": "Pasar Baru",
     "stop_lat": "-6.1620", "stop_lon": "106.8450"},
]

TRIPS = [
    {"route_id": "TJ-1", "service_id": "ALL", "trip_id": "TJ1-001",
     "direction_id": "0"},
    {"route_id": "TJ-1", "service_id": "ALL", "trip_id": "TJ1-002",
     "direction_id": "0"},
    {"route_id": "TJ-2", "service_id": "ALL", "trip_id": "TJ2-001",
     "direction_id": "0"},
    {"route_id": "TJ-3", "service_id": "ALL", "trip_id": "TJ3-001",
     "direction_id": "0"},
]

# Include one >24:00 time to test midnight-crossing parser
STOP_TIMES = [
    {"trip_id": "TJ1-001", "arrival_time": "06:00:00",
     "departure_time": "06:01:00", "stop_id": "BM", "stop_sequence": "1"},
    {"trip_id": "TJ1-001", "arrival_time": "06:15:00",
     "departure_time": "06:16:00", "stop_id": "MH", "stop_sequence": "2"},
    {"trip_id": "TJ1-001", "arrival_time": "06:35:00",
     "departure_time": "06:36:00", "stop_id": "BD", "stop_sequence": "3"},
    {"trip_id": "TJ1-001", "arrival_time": "07:10:00",
     "departure_time": "07:11:00", "stop_id": "KT", "stop_sequence": "4"},
    {"trip_id": "TJ1-002", "arrival_time": "25:00:00",
     "departure_time": "25:01:00", "stop_id": "BM", "stop_sequence": "1"},
    {"trip_id": "TJ1-002", "arrival_time": "25:20:00",
     "departure_time": "25:21:00", "stop_id": "MH", "stop_sequence": "2"},
    {"trip_id": "TJ2-001", "arrival_time": "07:30:00",
     "departure_time": "07:31:00", "stop_id": "PG", "stop_sequence": "1"},
    {"trip_id": "TJ2-001", "arrival_time": "08:00:00",
     "departure_time": "08:01:00", "stop_id": "HM", "stop_sequence": "2"},
    {"trip_id": "TJ3-001", "arrival_time": "08:15:00",
     "departure_time": "08:16:00", "stop_id": "KD", "stop_sequence": "1"},
    {"trip_id": "TJ3-001", "arrival_time": "08:50:00",
     "departure_time": "08:51:00", "stop_id": "PB", "stop_sequence": "2"},
]

FEED_INFO = [
    {"feed_publisher_name": "ITMA CI Generator",
     "feed_publisher_url": "https://github.com/arfan379/itma",
     "feed_lang": "id", "feed_version": "ci-sample-1.0"},
]


def _write_csv_to_buffer(rows, fieldnames):
    """Write list of dicts to an in-memory CSV string."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def generate_sample_gtfs_zip(output_path="data/sample_gtfs.zip"):
    """
    Create a minimal GTFS ZIP file suitable for CI testing.

    Args:
        output_path: Path to write the output ZIP file.

    Returns:
        str: Absolute path to the generated ZIP file.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    files = {
        "routes.txt": _write_csv_to_buffer(
            ROUTES,
            ["route_id", "agency_id", "route_short_name", "route_long_name", "route_type"],
        ),
        "stops.txt": _write_csv_to_buffer(
            STOPS,
            ["stop_id", "stop_name", "stop_lat", "stop_lon"],
        ),
        "trips.txt": _write_csv_to_buffer(
            TRIPS,
            ["route_id", "service_id", "trip_id", "direction_id"],
        ),
        "stop_times.txt": _write_csv_to_buffer(
            STOP_TIMES,
            ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
        ),
        "feed_info.txt": _write_csv_to_buffer(
            FEED_INFO,
            ["feed_publisher_name", "feed_publisher_url", "feed_lang", "feed_version"],
        ),
    }

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)

    return os.path.abspath(output_path)


if __name__ == "__main__":
    path = generate_sample_gtfs_zip()
    print(f"[sample_gtfs] Generated: {path}")
