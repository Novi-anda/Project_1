import dht
import network
import ntptime
import ujson
import utime

from machine import RTC
from machine import Pin
from time import sleep
from third_party import rd_jwt

from umqtt.simple import MQTTClient


# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "Novianda"
AP_PASSWORD = "999999999"

# Decoded Private Key
PRIVATE_KEY = (25076501472651336761524739132779737355391388064308475851352169153373397487884961134626082690851233161360812845305420947357444529938620721764807243624054178427796174951755766992795073544509995845697315392488823691443287751365965468019588761915174051783748111290224805377852221072508062619305591332005579680503085325574130285201508872347135824309026970592403513115522786872683566784755668998574262496014543133747287098963268221391430327292217737616146992861576705162876019069668807816186335394887972028651954506313817190856589906049889622743702299286187779701077911656722606886670817241248341919111475967681391763285631, 65537, 546779996100199280287758857145463550068729016340339228093782896992089735724668652232794790198306486222814617024603606112177674188356028066617476404760263987874341730717899675491770451731156202809122536824488900240664940365014642931473707078089990692265072417622583378625064069344248615026438348008544385056356777294900398995184933958097192068713468231141446252561081088327584992033520918816766489285212969266357025692143218751988906327843726059125169822512939141637348411391459116865360384734165278649139320107460224001174982500664743951450617196303787866957353107941532369063679295454963413713713382491379409076673, 174899791528908758469983418372586336990350827360730150641121319336123533972378800804317922630503501844672737448529052688768784750810502110836317613050814160417450483687931284741249304645102963348426902775422905593954713577446071032313615363354457641707190778710238703004834709401559376000371854849302710716191, 143376394296653596688282342468152872474291238578848007501979559138249672826075042770346666956466247151571399453164551943321476755616980266062071569008401481474031960814986998901262763214884553876905054985125775560042590550774325436917655795358622663440664450325729365383022429515125968894425352623878882759841)

#Project ID of IoT Core
PROJECT_ID = "hsc2020-03"
# Location of server
REGION_ID = "asia-east1"
# ID of IoT registry
REGISTRY_ID = "NPM_1704111010005"
# ID of this device
DEVICE_ID = "ESP32"

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "mqtt.googleapis.com"
MQTT_BRIDGE_PORT = 8883


dht22_obj = dht.DHT22(Pin(4))
led_obj = Pin(23, Pin.OUT)
def suhu_kelembaban():
    # Read temperature from DHT 22
    #
    # Return
    #    * List (temperature, humidity)
    #    * None if failed to read from sensor
    while True:
        try:
            dht22_obj.measure()
            return dht22_obj.temperature(),dht22_obj.humidity()
            sleep(3)
            break
        except:
            return None
def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
        wlan.connect(AP_SSID, AP_PASSWORD)
        # Loop until connected
        while not wlan.isconnected():
            pass
    
    # Connected
    print("  Connected:", wlan.ifconfig())


def set_time():
    # Update machine with NTP server
    print("Updating machine time...")

    # Loop until connected to NTP Server
    while True:
        try:
            # Connect to NTP server and set machine time
            ntptime.settime()
            # Success, break out off loop
            break
        except OSError as err:
            # Fail to connect to NTP Server
            print("  Fail to connect to NTP server, retrying (Error: {})....".format(err))
            # Wait before reattempting. Note: Better approach exponential instead of fix wiat time
            utime.sleep(0.5)
    
    # Succeeded in updating machine time
    print("  Time set to:", RTC().datetime())


def on_message(topic, message):
    print((topic,message))


def get_client(jwt):
    #Create our MQTT client.
    #
    # The client_id is a unique string that identifies this device.
    # For Google Cloud IoT Core, it must be in the format below.
    #
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    client = MQTTClient(client_id.encode('utf-8'),
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT,
                        user=b'ignored',
                        password=jwt.encode('utf-8'),
                        ssl=True)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'events')
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)
    
    
def subscribe_command():
    print("Sending command to device")
    # Subscribe to the events
    mqtt_topic = '/devices/{DEVICE_ID}/commands/#'
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    command = 'baca'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        humi = dht22_obj.humidity()
        print("Suhu: ", temp)
        print("Kelembaban: ", humi)
        sleep(3)

    # Subscribe to the config topic.
    

    
def subscribe_command1():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    command = 'PING!'
    data = command.encode("utf-8")
    while True:
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        break
def subscribe_command2():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    #ukur = f"/devices/{DEVICE_ID}/commands/#"
    command = 'Baca Suhu'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        print(temp)
        sleep(3)
    publish(client, temp)
def subscribe_command3():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    #ukur = f"/devices/{DEVICE_ID}/commands/#"
    command = 'Baca Kelembaban'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        humi = dht22_obj.humidity()
        print(humi)
        sleep(3)
    publish(client, humi)
# Connect to Wifi
connect()
# Set machine time to now
set_time()

# Create JWT Token
print("Creating JWT token.")
start_time = utime.time()
jwt = rd_jwt.create_jwt(PRIVATE_KEY, PROJECT_ID)
end_time = utime.time()
print("  Created token in", end_time - start_time, "seconds.")

# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client(jwt)
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")

# Read from DHT22
#print("Reading from DHT22")
#result1 = suhu_kelembaban()
#print("Suhu dan Kelembaban ", result1)
# Publish a message
#print("Publishing message...")
#if result1 == None:
  #result1 = "Fail to read sensor...."


#publish(client, result1)
# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()
#publish_events()
#publish_state()
#subscribe_config()
subscribe_command()
#subscribe_command1()
#subscribe_command2()
#subscribe_command3()