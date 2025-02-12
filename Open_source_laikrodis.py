# There are 2 options to select BLE device:
# 1. Scan for all BLE devices auto and pick PineTime watch
# 2. Hard-code PineTime watch MAC address value [MAC address can be found in About section on watch] -> DE:65:48:68:F9:55
import asyncio
from bleak import BleakScanner, BleakClient

# PineTime Heart Rate UUID
HEART_RATE_MEASUREMENT_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Store last known heart rate
last_heart_rate = None

# Scan for PineTime (can be removed if MAC address is hard-coded)
async def scan_for_pinetime():
    devices = await BleakScanner.discover(timeout=10)
    for device in devices:
        if device.name and "InfiniTime" in device.name:
            print(f"Found PineTime: {device.address}")
            return device.address
    print("PineTime not found")
    return None

# Heart rate notification handler
def heart_rate_handler(sender, data):
    global last_heart_rate
    if len(data) > 1:
        heart_rate = data[1]  # extract heart rate value
        if heart_rate != last_heart_rate:  # only log new HR values
            last_heart_rate = heart_rate
            print(f"Heart Rate: {last_heart_rate}") # for now just print result to console

# Connect and subscribe to heart rate notifications (runs indefinitely)
async def connect_and_subscribe(device_address):
    global last_heart_rate

    while True:  # Infinite loop until manually stopped
        try:
            async with BleakClient(device_address) as client:
                print("Connected to PineTime")

                # Start heart rate notifications
                await client.start_notify(HEART_RATE_MEASUREMENT_CHAR_UUID, heart_rate_handler)
                print("Subscribed to heart rate notifications...")

                while await client.is_connected():
                    await asyncio.sleep(5)  # keep the loop alive

        except Exception as e:
            print(f"Connection lost, retrying... Error: {e}")
            await asyncio.sleep(5)  # retry after 5 seconds

# Main (adjust if MAC address is used instead auto scanning)
async def main():
    device_address = await scan_for_pinetime()
    if device_address:
        await connect_and_subscribe(device_address)

# Run the script
asyncio.run(main())
