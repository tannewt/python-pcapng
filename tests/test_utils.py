from six import int2byte

from pcapng.utils import (
    pack_timestamp_resolution, unpack_euiaddr, unpack_ipv4, unpack_ipv6,
    unpack_macaddr, unpack_timestamp_resolution)


def test_unpack_ipv4():
    assert unpack_ipv4('\x00\x00\x00\x00') == '0.0.0.0'
    assert unpack_ipv4('\xff\xff\xff\xff') == '255.255.255.255'
    assert unpack_ipv4('\x0a\x10\x20\x30') == '10.16.32.48'


def test_unpack_ipv6():
    assert unpack_ipv6('\x00\x11\x22\x33\x44\x55\x66\x77'
                       '\x88\x99\xaa\xbb\xcc\xdd\xee\xff') \
        == '0011:2233:4455:6677:8899:aabb:ccdd:eeff'


def test_unpack_macaddr():
    assert unpack_macaddr('\x00\x11\x22\xaa\xbb\xcc') == \
        '00:11:22:aa:bb:cc'


def test_unpack_euiaddr():
    assert unpack_euiaddr('\x00\x11\x22\x33\xaa\xbb\xcc\xdd') == \
        '00:11:22:33:aa:bb:cc:dd'


def test_unpack_tsresol():
    assert unpack_timestamp_resolution(int2byte(0)) == 1
    assert unpack_timestamp_resolution(int2byte(1)) == 1e-1
    assert unpack_timestamp_resolution(int2byte(6)) == 1e-6
    assert unpack_timestamp_resolution(int2byte(100)) == 1e-100

    assert unpack_timestamp_resolution(int2byte(0 | 0b10000000)) == 1
    assert unpack_timestamp_resolution(int2byte(1 | 0b10000000)) == 2 ** -1
    assert unpack_timestamp_resolution(int2byte(6 | 0b10000000)) == 2 ** -6
    assert unpack_timestamp_resolution(int2byte(100 | 0b10000000)) == 2 ** -100


def test_pack_tsresol():
    assert pack_timestamp_resolution(10, 0b00000000) == int2byte(0b00000000)
    assert pack_timestamp_resolution(10, 0b00000011) == int2byte(0b00000011)
    assert pack_timestamp_resolution(10, 0b00000100) == int2byte(0b00000100)
    assert pack_timestamp_resolution(10, 0b00111100) == int2byte(0b00111100)

    assert pack_timestamp_resolution(2, 0b00000000) == int2byte(0b10000000)
    assert pack_timestamp_resolution(2, 0b00000011) == int2byte(0b10000011)
    assert pack_timestamp_resolution(2, 0b00000100) == int2byte(0b10000100)
    assert pack_timestamp_resolution(2, 0b00111100) == int2byte(0b10111100)
