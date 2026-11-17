# Internet speed test

Console script (Python 3.9+, standard library only) that measures download speed.

It makes 10 sequential requests to the given URL, reads each full response,
and prints the average request time, total downloaded data and download speed.

## Usage

```bash
python3 speedtest.py <url>
python3 speedtest.py https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg
```

Optional: `-n 5` changes the number of requests (default 10).

## Example output

```
Request  1: 8.12 MB in 0.912 s
...
Request 10: 8.12 MB in 0.874 s

Average request time: 0.893 s
Total downloaded:     81.20 MB
Download speed:       72.75 Mbit/s
```

## Units

- Time: seconds (s)
- Data volume: megabytes (MB, 1 MB = 1,000,000 bytes)
- Speed: **megabits per second (Mbit/s)**, the unit ISPs use.
  Calculated as `total bytes * 8 / total request time / 1,000,000`.

## Notes

- Time per request covers connection setup, headers and the full body download.
- If a request fails, the script reports the error and exits with code 1.
- Use a large file so transfer time dominates over latency.
