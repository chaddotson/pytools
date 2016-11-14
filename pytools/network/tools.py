from collections import namedtuple
from subprocess import Popen, PIPE
from re import compile, IGNORECASE, MULTILINE
from urllib.request import urlopen

from six.moves.urllib.request import urlopen


# min/avg/max/stddev
PING_RESULTS_PATTERN = b"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)"
PACKET_LOSS_PATTERN = b"(\d+\.?\d+)%"
compiled_ping_results_pattern = compile(PING_RESULTS_PATTERN, IGNORECASE)
compiled_packet_loss_pattern = compile(PACKET_LOSS_PATTERN, IGNORECASE)


class PingResults(namedtuple("PingResults", ["host", "count", "min", "max", "avg", "stddev", "percent_packet_loss"])):
    def __new__(cls, host, count, min=None, max=None, avg=None, stddev=None, percent_packet_loss=None):
        return super(PingResults, cls).__new__(cls, host, count, min, max, avg, stddev, percent_packet_loss)

    def __str__(self):
        return "Ping Results - host: {0.host} min/max/avg: {0.min}/{0.max}/{0.avg} loss: {0.percent_packet_loss}%".format(self)

    def __repr__(self):
        return "{0}(host={1.host}, min={1.min}, max={1.max}, avg={1.avg}, stddev={1.stddev}, percent_packet_loss={1.percent_packet_loss}%)".format(self.__class__.__name__, self)


class PingFailedError(RuntimeError):
    def __init__(self, host):
        super(PingFailedError, self).__init__("Failed to ping {0}.  Host possibly down.".format(host))


def ping(host, ping_count=3):
    call_list = ["ping", "-c", str(ping_count), host]
    process = Popen(call_list, stdout=PIPE)
    results, err = process.communicate()
    time_results = compiled_ping_results_pattern.search(results)
    packet_loss_results = compiled_packet_loss_pattern.search(results)
    if time_results is None:
        raise PingFailedError(host)
    time_result_matches = time_results.groups()
    packet_loss_matches = packet_loss_results.groups()
    return PingResults(host=host,
                       count=ping_count,
                       min=float(time_result_matches[0]),
                       avg=float(time_result_matches[1]),
                       max=float(time_result_matches[2]),
                       stddev=float(time_result_matches[3]),
                       percent_packet_loss=float(packet_loss_matches[0]))


def is_online(host, ping_count=3):
    try:
        results = ping(host, ping_count=ping_count)
        return results.percent_packet_loss < 100.0

    except PingFailedError:
        return False


def get_external_ip_address():
    response = urlopen('http://www.myglobalip.com/')
    codec = response.info().get_param('charset', 'utf8')

    html = response.read()
    html = html.decode(codec)

    regex = compile("<span class=\"ip\">(.*?)</span>", MULTILINE)

    results = regex.search(html)

    ip_address = results.groups()[0]

    return ip_address