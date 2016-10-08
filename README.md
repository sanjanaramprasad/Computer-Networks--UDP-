# Computer-Networks--UDP-
UDP client program that sends data to a server on a specified port. The server echoes back the duplicated contents. For the request and response, the checksum is calculated which is verified and displayed by taking a tcpdump. Subsequently, a second request is made by appending 6 characters to the original data. By ensuring the checksum remains the same and that the first four characters matches the original input, the two remaining characters are computed.
