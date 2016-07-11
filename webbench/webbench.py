"""
The MIT License (MIT)

Copyright (c) 2016 Artem Rozumenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import sys
import socket
import ssl
import time
from multiprocessing import Pool


def bench_wrapper(kwargs):
    """
    Wrapper to call bench to extract arguments

    Returns:
        whatever bench returns
    """
    return bench(**kwargs)


def communicate(s, msg):
    """
    send message to socket and receive response
    :param s Socket Connection: - open socket
    :param msg: message
    :return str - response data
    """
    s.send(msg)
    return s.recv(1024)


def bench(host, port, uri, method, headers, body, verbocity, http_version):
    """
    The benchmark method
    :param host str: - host to run tests agains
    :param port int: - port to connect
    :param uri str: - URI to send in message
    :param method str: - http method
    :param headers str: - formatted headers for message
    :param body str: - body of message
    :param verbocity int [0-1]: - print extended output option
    :param http_version str: - represetation of http protocol
    :return
        [list] results of benchmark:
    """
    t1 = time.time()
    s = create_connction(host, port)
    t2 = time.time()

    msg = "%s %s HTTP/%s\r\n" % (method, uri, http_version)
    if body:
        body='%s\r\n' % body
        msg += "Content-length: %s\r\n" % len(body)
    msg += headers
    msg += "\r\n"
    msg += "\r\n"
    msg += body
    if verbocity:
        print msg
    res = ''
    t3 = time.time()
    data = communicate(s, msg)
    if verbocity:
        if 'gzip' in data:
            data = data.split("\r\n\r\n", 1)
            print data[0]
            print
            print data[1]
        else:
            print data
    t4 = time.time()
    res += "%s,%s,ms,%s,ms,%s,ms\n" % (host, round((t4 - t1) * 1000.0, 3),
                                       round((t2 - t1) * 1000.0, 3),
                                       round((t4 - t3) * 1000.0, 3))
    s.close()
    return res


def create_connction(host, port):
    """
    Create connection to socket host/port
    :param host srt: - host to connect
    :param port int: - port to connect
    :return socket: - open connection
    """
    ai_list = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
                                 socket.SOCK_STREAM)
    for (family, socktype, proto, canon, sockaddr) in ai_list:
        sock = socket.socket(family, socktype)
        # WRAP SOCKET
        if port == 443:
            sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
        sock.connect(sockaddr)
        return sock


def main():
    """Mein methos of pybench executor"""
    parser = argparse.ArgumentParser(description='webBench is an alternative to ab in python')

    parser.add_argument('-n', dest='requests', type=int,
                        help='Number of requests to perform')
    parser.add_argument('-c', dest='concurrency', type=int,
                        help='Number of multiple requests to make at a time')
    parser.add_argument('-d', dest='strbody', type=str, default='',
                        help='String post body')
    parser.add_argument('-p', dest='postfile', type=str, default='',
                        help='File containing data to POST')
    parser.add_argument('-u', dest='putfile', type=str, default='',
                        help='File containing data to PUT')
    parser.add_argument('-v', dest='verbosity', type=int, default=0,
                        help='How much troubleshooting info to print')
    parser.add_argument('-H', dest='header', action='append', default=[],
                        help='Add Arbitrary header line, eg. "Accept-Encoding: gzip"\n'
                             'Inserted after all normal header lines. (repeatable)')
    parser.add_argument('-e', dest='csv', type=str, default='',
                        help='Output CSV file with percentages served')
    parser.add_argument('-m', dest='method', type=str, default='GET',
                        help='Method name')
    parser.add_argument('-Z', dest='ciphersuite', type=str, default='',
                        help='Specify SSL/TLS cipher suite (See openssl ciphers)')
    parser.add_argument('-t', dest='http_version', default='1.1',
                        help='Speofy HTTP versions (1.0, 1.1)')
    parser.add_argument('-f', dest='protocol', default='SSLv23',
                        help='Specify SSL/TLS protocol (SSLv23, SSLv2, SSLv3, TLSv1)')
    parser.add_argument('url', metavar="URL", type=str, help='URL of request')

    # args = parser.parse_args(["-c", "1", "-n", "1", "-v", "1", "-H",
    #                           "Content-Type: application/x-www-form-urlencoded;charset=utf-8",
    #                           "-H", "Host: upl.pa.dev",
    #                           "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) "
    #                                 "Gecko/20100101 Firefox/47.0",
    #                           "-H", "Accept: application/json, text/plain, */*'",
    #                           "-H 'Accept-Language: en-US,en;q=0.5",
    #                           "-H", "Accept-Encoding: gzip, deflate, br",
    #                           "-H", "X-XSRF-TOKEN: f005bad9fcec4dec745917b37b8495154f8eed0ed4fa220f3df3be79"
    #                                 "b457a33c1f76696b6e33488d67cfa29d375d65c00813ca8b4c53cf39a3e7225d64610de7",
    #                           "-H", "Referer: https://upl.pa.dev/",
    #                           "-H", "Cookie: PHPSESSID=inhevvko89k92ls80skc7ii3h6; "
    #                                 "idpSAMLSessionID=e8342db3073f8320f5a4089a9adc6cf6; "
    #                                 "idpSAMLAuthToken=_b2a7d9935241b6b8862e2e393b26cc4d304e64c0b9; "
    #                                 "spSAMLSessionID=870b591c8ff5ffde5b1a3dc7bc981c1a; "
    #                                 "spSAMLAuthToken=_70f436ee6e64911a7fa6d03d0e3faa57b2d822b4c6; "
    #                                 "XSRF-TOKEN=f005bad9fcec4dec745917b37b8495154f8eed0ed4fa220f3d"
    #                                 "f3be79b457a33c1f76696b6e33488d67cfa29d375d65c00813ca8b4c53cf39a3"
    #                                 "e7225d64610de7; "
    #                                 "web_token=29380664226a1933f9c33684f5c81b5267cab4fcfb84ea44603d8d9b7"
    #                                 "8529b7d22fc47c7011a7abf69358ff1a7dcc63c924513ab71eb22381689864fb1724292",
    #                           "-H", "Connection: keep-alive",
    #                           "-p", "/tmp/test.body", "https://upl.pa.dev/webapi/workspacefile/getProperties"])
    args = parser.parse_args()

    if args.requests < args.concurrency:
        print "Requests should be bigger then concurrency"
        sys.exit(1)
    arguments = []
    method = args.method
    port = 443 if 'https' in args.url else 80
    host = args.url[args.url.index("://") + 3:]
    uri = '/'
    body = ''
    headers = '\r\n'.join(args.header) if args.header else []
    if '/' in host:
        uri = '%s' % host[host.index("/"):]
        host = host[:host.index("/")]
    if args.strbody:
        body = args.strbody
        method = 'POST'
    if args.postfile:
        with open(args.postfile, 'r') as f:
            body = f.read().strip()
        method = 'POST'
    elif args.putfile:
        with open(args.putfile, 'r') as f:
            body = f.read().strip()
        method = 'PUT'

    print "Starting benchmark for:"
    print "%s %s %s" % (method, args.url, args.http_version)
    if args.verbosity:
        if headers:
            print " Headers: \n%s" % headers
            print
        if body:
            print "Body: \n%s" % body
    print
    p = Pool(args.concurrency)
    for each in range(args.requests):
        arguments.append(dict(host=host, port=port, uri=uri, headers=headers,
                              verbocity=True if args.verbosity else False,
                              body=body, method=method, http_version=args.http_version))
    print "Staring test ... "
    result = []
    start = time.time()
    for each in p.imap_unordered(bench_wrapper, arguments):
        result.append(each)
        if start + 1 < time.time():
            start = time.time()
            print "Remaining %s requests ... " % (args.requests - len(result))
    if args.csv:
        with open(args.csv, 'w') as f:
            f.write("".join(result))
    print
    print
    if args.verbosity:
        print "".join(result)
        print
        print
    req_time = []
    connection_time = []
    processing_time = []
    for each in result:
        if ',' in each:
            tmp_res = each.split(',')
            req_time.append(float(tmp_res[1]))
            connection_time.append(float(tmp_res[3]))
            processing_time.append(float(tmp_res[5]))

    print 'Summary:'
    print 'Failed Requests: %s ' % (args.requests - len(req_time))
    print
    print "Percentile\tConnection,ms\tProcessing,ms\tTotal,ms"
    some_chart = sorted(req_time)
    le = len(some_chart)
    for per in [0.5, 0.66, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99]:
        value = some_chart[int(per*float(le))]
        index = req_time.index(value)
        print "%s %%\t\t%s\t\t%s\t\t%s" % (per*100, connection_time[index], processing_time[index], req_time[index])
    print "%s %%\t\t%s\t\t%s\t\t%s" % (100, max(connection_time), max(processing_time), max(req_time))
    print


if __name__ == "__main__":
    main()

