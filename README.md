# bitcoin-wireshark

A wireshark dissector for the bitcoin protocol.

The packet-bitcoin.c dissector was originally taken from https://github.com/wireshark/wireshark/commit/d4eeeaf6d463f930c89e9026b682339e1e114b34

## Build instructions:

- Download wireshark source either from http://www.wireshark.org/download/src/all-versions/ or https://github.com/wireshark/wireshark
- Clone this repository (outside the wireshark directory)
- Copy the packet-bitcoin.c file from this repository into epan/dissectors in the wireshark directory (either copying the file or creating a symlink)
- Rebuild Wireshark by running `make && sudo make install`
- run the decoder test in this repository `./test-decoder`

## Wireshark dependencies

Building wireshark has a lot of dependencies. On ubuntu, I had to apt-get the following: 

- `automake`
- `autoconf`
- `pkg-config`
- `libtool-bin`
- `python`
- `bison`
- `byacc`
- `flex`
- `libglib2.0-dev`
- `libqt4-designer libqt4-opengl libqt4-svg libqtgui4 libqtwebkit4`
- `qt4-dev-tools`
- `libpcap-dev`

