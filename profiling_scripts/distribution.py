import scipy.stats as stats
import time

import RoomDict.RoomDict as RoomDict

DATA_SIZE = int(1e7)
DATA_SIZE = int(1e2)
CACHE_SIZE = 0.01 * DATA_SIZE
DELAYS = [0.001, 0.01, 0.1]
ERROR_RATES = [0.01, 0.1, 0.5]

def profile_data(data, **log_kwargs):
    for error_rate in ERROR_RATES:
        for delay in DELAYS:
            for use_bloom in [False, True]:
                cache_policies = ["lru", "none"]
                cache_kwargs = [{"max_size": CACHE_SIZE}]
                storage_backends = ["memory", "arbitrary"]
                storage_kwargs = [{}, {"delay": delay}]

                if use_bloom:
                    membership_tests = ["none", "bloom"]
                    membership_test_kwargs = [{}, {"max_size": DATA_SIZE, "error_rate": error_rate}]
                else:
                    membership_tests = ["none", "none"]
                    membership_test_kwargs = []

                with RoomDict(
                    cache_policies,
                    membership_tests,
                    storage_backends,
                    cache_kwargs,
                    membership_test_kwargs,
                    storage_kwargs,
                ) as cache:
                    start = time.time()
                    for key in data:
                        key = str(key)
                        if key in cache:
                            cache[key] += 1
                        else:
                            cache[key] = 1
                    end = time.time()

                profiling_log = {
                        "DATA_SIZE": DATA_SIZE,
                        "CACHE_SIZE": CACHE_SIZE,
                        **log_kwargs,
                        "BLOOM": use_bloom,
                        "TIME": end-start,
                        }
                print("$$".join(["{}_{}".format(key, value) for key, value in profiling_log.items()]))

                # time.sleep(10)

# Profile zipf distribution.
zipf_scales = [1.01, 1.05, 1.1, 1.2]
for scale in zipf_scales:
    zipf_data = stats.zipf.rvs(scale, size=DATA_SIZE)

    log_kwargs = {
            "DISTRIBUTION": "zipf",
            "SCALE": scale,
            }
    profile_data(zipf_data, **log_kwargs)

# Profile uniform distribution.
scale = DATA_SIZE
uniform_data = stats.uniform.rvs(0, scale, size=DATA_SIZE)
log_kwargs = {
        "DISTRIBUTION": "uniform",
        "SCALE": scale,
        }
profile_data(uniform_data, **log_kwargs)
