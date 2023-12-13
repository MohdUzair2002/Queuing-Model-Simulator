import math
from scipy import stats
from queuing_simulator import constants as const
import numpy as np
import random


def get_service_time(
    service_dist_type,
    service_mean,
    service_variance,
):
    if service_dist_type == const.EXP_POIS_RAND_DIST:
        return abs(np.random.exponential(scale= service_mean))
    if service_dist_type == const.NORMAL_DIST:
        return abs(
            np.random.normal(loc=service_mean, scale=math.sqrt(service_variance))
        )
    if service_dist_type == const.UNIFORM_DIST:
        a = service_mean - math.sqrt(3 * service_variance)
        b = service_mean + math.sqrt(3 * service_variance)
        return abs(np.random.uniform(low=a, high=b))
    shape = service_mean**2 / service_variance
    scale = service_variance / service_mean
    return abs(np.random.gamma(shape, scale))


def calculate_cdf(x, arrival_dist_type, arrival_mean, arrival_variance):
    if arrival_dist_type == const.EXP_POIS_RAND_DIST:
        return stats.poisson.cdf(x, arrival_mean)
    if arrival_dist_type == const.NORMAL_DIST:
        return stats.norm.cdf(x, loc=arrival_mean, scale=math.sqrt(arrival_variance))
    if arrival_dist_type == const.UNIFORM_DIST:
        a = arrival_mean - math.sqrt(3 * arrival_variance)
        b = arrival_mean + math.sqrt(3 * arrival_variance)
        return stats.uniform.cdf(x, loc=a, scale=b - a)
    k = arrival_mean**2 / arrival_variance
    theta = arrival_variance / arrival_mean
    return stats.gamma.cdf(x, k, loc=0, scale=theta)


def calculate_poisson_cdf(k, mean):
    cdf = 0.0
    for i in range(k + 1):
        cdf += (mean**i) * math.exp(-mean) / math.factorial(i)
    return cdf


def calculate_service_time(random_num, mean):
    return math.ceil(-(math.log(1 - random_num)) / mean)


def get_inter_arrival_time(random_num, df_avg_arrival_time_lookup):
    for index, row in df_avg_arrival_time_lookup.iterrows():
        if random_num >= row.cum_prob_lookup and random_num < row.cum_prob:
            return row.inter_arrival_time


def is_server_idle(arrival_time, server):
    return len(server) == 0 or server[-1]["end"] <= arrival_time


def find_server_index_with_min_time_left(servers):
    return servers.index(min(servers, key=lambda server: server[-1]["end"]))
