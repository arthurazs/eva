from asyncio import open_connection, wait_for
from asyncio import sleep, get_event_loop
from struct import pack


async def tcp_echo_client(loop):

    stream_in, stream_out = await wait_for(
        open_connection('10.0.1.3', 102, loop=loop), timeout=3)

    await stream_in.read(1024)
    print('Recv: COTP')

    data = pack('22B', 0x03, 0x00, 0x00, 0x16, 0x11, 0xd0, 0x00, 0x01, 0x14,
                0x00, 0x00, 0xc1, 0x02, 0x00, 0x01, 0xc2, 0x02, 0x00, 0x01,
                0xc0, 0x01, 0x0a)
    stream_out.write(data)
    print('Sent: CTOP')

    await stream_in.read(1024)
    print('Recv: MMS-Initiate')

    data = pack('162B', 0x03, 0x00, 0x00, 0xa2, 0x02, 0xf0, 0x80, 0x0e, 0x99,
                0x05, 0x06, 0x13, 0x01, 0x00, 0x16, 0x01, 0x02, 0x14, 0x02,
                0x00, 0x02, 0xc1, 0x8b, 0x31, 0x81, 0x88, 0xa0, 0x03, 0x80,
                0x01, 0x01, 0xa2, 0x81, 0x80, 0x83, 0x04, 0x00, 0x00, 0x00,
                0x01, 0xa5, 0x12, 0x30, 0x07, 0x80, 0x01, 0x00, 0x81, 0x02,
                0x51, 0x01, 0x30, 0x07, 0x80, 0x01, 0x00, 0x81, 0x02, 0x51,
                0x01, 0x88, 0x02, 0x06, 0x00, 0x61, 0x60, 0x30, 0x5e, 0x02,
                0x01, 0x01, 0xa0, 0x59, 0x61, 0x57, 0x80, 0x02, 0x07, 0x80,
                0xa1, 0x07, 0x06, 0x05, 0x28, 0xca, 0x22, 0x02, 0x03, 0xa2,
                0x03, 0x02, 0x01, 0x00, 0xa3, 0x05, 0xa1, 0x03, 0x02, 0x01,
                0x00, 0xa4, 0x07, 0x06, 0x05, 0x29, 0x01, 0x87, 0x67, 0x01,
                0xa5, 0x03, 0x02, 0x01, 0x0c, 0xbe, 0x2e, 0x28, 0x2c, 0x02,
                0x01, 0x03, 0xa0, 0x27, 0xa9, 0x25, 0x80, 0x02, 0x2e, 0xe0,
                0x81, 0x01, 0x01, 0x82, 0x01, 0x03, 0x83, 0x01, 0x08, 0xa4,
                0x16, 0x80, 0x01, 0x01, 0x81, 0x03, 0x05, 0xf1, 0x00, 0x82,
                0x0c, 0x03, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x10)
    stream_out.write(data)
    print('Sent: MMS-Initiate')

    await stream_in.read(1024)
    print('Recv: MMS-Read >>> ChargingLD/DRCT.Comm.function')

    data = pack('39B', 0x03, 0x00, 0x00, 0x27,  # quantos bytes esse pack
                0x02, 0xf0, 0x80, 0x01, 0x00, 0x01, 0x00,
                0x61, 0x1A,  # quantos bytes a baixo
                0x30, 0x18,  # quantos bytes a baixo
                0x02, 0x01, 0x03, 0xa0, 0x13,  # quantos bytes a baixo
                0xa1, 0x11, 0x02, 0x01, 0x01,
                0xa4, 0x0c, 0xa1, 0x0a,
                0x8a, 0x08, 0x52, 0x65, 0x63, 0x68, 0x61, 0x72, 0x67, 0x65)
    stream_out.write(data)
    print('Sent: MMS-Read >>> Recharge')

    data = await stream_in.read(1024)
    print('Recv: MMS-Write >>> BatteryLD/ZBTC.BatChaSt.setVal->2')

    data = pack('29B', 0x03, 0x00, 0x00, 0x1d, 0x02, 0xf0, 0x80, 0x01, 0x00,
                0x01, 0x00, 0x61, 0x10, 0x30, 0x0e, 0x02, 0x01, 0x03, 0xa0,
                0x09, 0xa1, 0x07, 0x02, 0x01, 0x02, 0xa5, 0x02, 0x81, 0x00)
    stream_out.write(data)
    print('Sent: MMS-Write >>> Success')

    # await sleep(10)

    print('Closing the socket')
    stream_out.close()


loop = get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()
