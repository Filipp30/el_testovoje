#!/usr/bin/env python3
"""Console tool that measures download speed by requesting a URL several times."""

import argparse
import sys
import time
import urllib.error
import urllib.request

CHUNK_SIZE = 64 * 1024
TIMEOUT = 30


def fetch(url: str) -> tuple[int, float]:
    """Download the full response body. Returns (bytes_received, seconds)."""
    request = urllib.request.Request(url, headers={"User-Agent": "speedtest-cli/1.0", "Cache-Control": "no-cache"})
    start = time.perf_counter()
    total = 0
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            total += len(chunk)
    return total, time.perf_counter() - start


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure download speed of a URL.")
    parser.add_argument("url", help="address to request (e.g. a large image)")
    parser.add_argument("-n", "--requests", type=int, default=10, help="number of requests (default: 10)")
    args = parser.parse_args()

    if args.requests < 1:
        parser.error("--requests must be >= 1")

    total_bytes = 0
    total_time = 0.0

    for i in range(1, args.requests + 1):
        try:
            size, elapsed = fetch(args.url)
        except (urllib.error.URLError, ValueError, OSError) as exc:
            print(f"Request {i} failed: {exc}", file=sys.stderr)
            return 1
        total_bytes += size
        total_time += elapsed
        print(f"Request {i:>2}: {size / 1_000_000:.2f} MB in {elapsed:.3f} s")

    if total_time == 0:
        print("Total time is zero, cannot compute speed", file=sys.stderr)
        return 1

    avg_time = total_time / args.requests
    mbit_s = total_bytes * 8 / total_time / 1_000_000

    print()
    print(f"Average request time: {avg_time:.3f} s")
    print(f"Total downloaded:     {total_bytes / 1_000_000:.2f} MB")
    print(f"Download speed:       {mbit_s:.2f} Mbit/s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
