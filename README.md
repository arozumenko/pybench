# pybench
lightweight HTTP/HTTPS benchmark tool written on Python
it is an alternative to ab in python. Created to be able to see every connection Connection-Time :) 
helps a lot in debugging of performance issues.

positional arguments:
  URL              URL of request

optional arguments:
  -h, --help       show this help message and exit
  -n REQUESTS      Number of requests to perform
  -c CONCURRENCY   Number of multiple requests to make at a time
  -d STRBODY       String post body
  -p POSTFILE      File containing data to POST
  -u PUTFILE       File containing data to PUT
  -v VERBOSITY     How much troubleshooting info to print
  -H HEADER        Add Arbitrary header line, eg. "Accept-Encoding: gzip"
                   Inserted after all normal header lines. (repeatable)
  -e CSV           Output CSV file with percentages served
  -m METHOD        Method name
  -Z CIPHERSUITE   Specify SSL/TLS cipher suite (See openssl ciphers)
  -t HTTP_VERSION  Speofy HTTP versions (1.0, 1.1)
  -f PROTOCOL      Specify SSL/TLS protocol (SSLv23, SSLv2, SSLv3, TLSv1)
