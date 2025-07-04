# :wastebasket: Smart Trashcan
By: Sofia Emma Ashley Svensson (ssjr26)  
Level: Beginner  
Approximated time: 20-30h

## :pencil: Project Description
This project aims to build an intelligent and accessible Smart Trashcan prototype using the Raspberry Pi Pico microcontroller. The design incorporates multiple sensors and smart features to improve usability, accessibility, and maintenance notification, as well as data documentation. The main features used are an Automatic lid using a Distance Sensor, functionality of the lid opening with a servo motor, trash Level monitoring with notification using an Obstancle detection sensor and environmental monitoring using Temperature and humidity.

## :pushpin: Objective
### Why I chose this project
I chose this project because I wanted to take an everyday object and make it more optimal for daily life. I was specifically interested in improving something commonly used and found in every household. As a busy student living alone, I realized that it's easy to overlook simple tasks such as taking out the trash. This gave me the idea of creating a smart trashcan that not only serves it's main purpose but also helps manage people's waste more effectively.

### Purpose of the project
The purpose of this project is to develop a smart trashcan that can provide reminders when the trash is full or knowing when certain environmental conditions occur, conditions that make bad odor that could discourage people from using the trashcan. This project aims to improve household hygiene, making it more convenient and reminding people of a task that is often neglected.

### Insights it will give
* Gaining more knowledge in how microcontrollers and sensors work together
* How to visualize data via a platform
* How to create responsive and helpful device to solve real-life problems using the Raspberry Pi Pico

## :paperclip: Materials
:::info
:coin: **Overall budget:** 600-700kr  
:package: Materials that I already owned was cardboard, tape, glue and metal rod for the hinges of the lid.
:::

This table shows all the materials I have used, their purpose, cost and links of where I bought them from.

|                   Materials                   |           Purpose           | Cost | Links                                                                                                                               |
|:---------------------------------------------:|:---------------------------:|:----:| ----------------------------------------------------------------------------------------------------------------------------------- |
|             Raspberry Pi Pico WH              |       microcontroller       | 89kr | [link](https://www.electrokit.com/raspberry-pi-pico-w)                                                                              |
|              Wires (male/female)              |         connecting          | 49kr | [link](https://www.electrokit.com/labbsladd-20-pin-15cm-hona/hane)                                                                  |
|               Wires (male/male)               |         connecting          | 55kr | [link](https://www.electrokit.com/labbsladd-20-pin-15cm-hona/hona)                                                                  |
|                  Breadboard                   |  connecting the components  | 69kr | [link](https://www.electrokit.com/kopplingsdack-840-anslutningar)                                                                   |
|               Servo motor 180°                | opening and closing the lid | 99kr | [link](https://www.electrokit.com/mg90s-micro-servo)                                                                                |
|          Ultrasonic distance sensor           |      for automatic lid      | 59kr | [link](https://www.electrokit.com/avstandsmatare-ultraljud-hc-sr04-2-400cm)                                                         |
|           Obstacle detection sensor           |  detecting trash fullness   | 39kr | [link](https://www.electrokit.com/en/kollisionssensor-ir?srsltid=AfmBOornaQWyvAtiCyGJIC3A_L2I-_CaNtPcLEQqloj2hbdK2dG1ZeIQXyc&gQT=1) |
|                2-color 5mm LED                |         lid status          | 18kr | [link](https://www.electrokit.com/led-modul-rod/gron-5mm)                                                                           |
| Combination sensor (temperature and humidity) |  temperature and humidity   | 49kr | [link](https://www.electrokit.com/digital-temperatur-och-fuktsensor-dht11)                                                          |
|             2x  330 ohm Resistors             |            power            | 4kr  | [link](https://www.electrokit.com/motstand-1w-5330ohm-330r)                                                                         |

## :computer: Computer Setup
:::info
:bell: The tools I used for my setup are:  
* **Thonny**
* **Micropython firmware**  

To upload code, I flashed the micropython firmware into the pico and I can just code directly using Thonny.
:::

### Thonny
I used Thonny for this project as it is easy to use and very beginner friendly, which can be downloaded [here](https://thonny.org/)

### Micropython firmware
The only other tool you need is the micropython firmware so you could run python in the Raspberry Pi Pico WH and can upload from computer, which can be dowloaded [here](https://micropython.org/download/RPI_PICO/)

## :hammer: Putting everything together
### Circuit diagram
The following illustration shows an overview of the wiring and connections between the sensors, the microcontroller and the other components used for this project.
![SmartTrashcan](https://hackmd.io/_uploads/r1V4_fJSgl.png)

:::info
:memo: **Circuit calculations:** It is important for this project to ensure that the total power consumption does not exceed the capabilities that the Raspberry Pi Pico has.  

**Using ohms law**  
* **R = V / I**  

|                   Component                   |  Voltage   |  Current   |
|:---------------------------------------------:|:----------:|:----------:|
|             Raspberry Pi Pico WH              |    3.3V    |   90 mA    |
|               Servo motor 180°                | 4.8 - 6.0V | 100-250 mA |
|          Ultrasonic distance sensor           |     5V     |   15 mA    |
|           Obstacle detection sensor           |     5V     |   20 mA    |
|                2-color 5mm LED                |     5V     |    4 mA    |
| Combination sensor (temperature and humidity) |  3.3 - 5V  |   2.5 mA   |

:::

## :cloud: Code snippets
**Lid status**: The lid will automatically open when the distance sensor detects an object within 10 cm or less, otherwise the lid will stay closed. It will also publish in Adafruit IO whenever it's open or closed, but it will only actually publish if the lid state has changed.
``` Python
    lid_state = "open" if distance <= 10 else "closed"  #what the lid state is based on distance
    if lid_state != finallid_state:  #if the lid status changed
        publish(AIO_FEEDS["lid"], lid_state)  #if lid satus changed then publish
        finallid_state = lid_state  #update
```
**Servo motor and Led**: The motor will go 0 degrees to "open" the lid or else it will go to 90 degrees to close. Additionally, When it's "open", the LED will turn green and if it's "closed" then it will turn red.
``` Python
if lid_state == "open":
        Green.value(1)  #LED turns green
        Red.value(0)
        servo.set_angle(0)  #opens the lid
    else:
        Red.value(1)  #LED turns red
        Green.value(0)
        servo.set_angle(90)  #closes the lid
```
**Obstacle Detection sensor**: If the obstacle sensor detects an object for more than 5 seconds then it indicates that the trashcan is "full" otherwise its considered "not_full".
``` Python
trashisFull = 5 #number of seconds
...
obstacle_state = None  #initialize 
    if obstacle_detected:  #if triggered 
        if obstacle_starttime is None: 
            obstacle_starttime = current_time  #start timer 
        elif current_time - obstacle_starttime >= trashisFull:  #if the sensor is triggered for 5 or more seconds
            obstacle_state = "full"  #state is full
    else:
        obstacle_state = "not_full"  #otherwise not full
        obstacle_starttime = None
```
**Temperature and Humidity**: It will print out the temperature and humidity in Adafruit IO every 3 seconds in a graph in the dashboard. 
``` Python
temp, hum = temphum_sensor.read()  #read the temperature and humidity sensor
    if temp is not None and hum is not None:  #check
        adafruit.publish(AIO_FEEDS["temp"], temp)  #publish for temperature
        adafruit.publish(AIO_FEEDS["hum"], hum)  #publish for humidity
```
### Platform
I chose Adafruit IO as my platform, which is a cloud-based IoT platform that has easy data visualization, device communication over the internet and can be used for monitoring. I am currectly using the free version as it is suitable for small projects, such as mine and all dashboards/feeds are handled online so no local installations are needed.

I created a feed for each data I wanted (temperature, humidity, trash status, lid status), afterwards I made a dashboard to visualize the data and lastly I also created an action where everytime the trash is "full" then it will send a message through discord.

I did consider other platforms such as Blynk but overall I think Adafruit IO is the best option for this project because it is easy, quick and scalable. For the future, if I wanted to scale my idea, I would need to pay subscription in Adafruit IO, but I could also start hosting my own server for further educational development.

## :abacus: Transmitting the data/connectivity
When it comes to the temperature and humidity data, the data is sent to Adafruit IO regularly every 3 seconds while the lid status and trash status is sent when the status is changed.

In this project, data from the smart trashcan is transmitted using the **built in Wifi** in the Raspberry Pi Pico microcontroller since it was readily available and there were no requirement for additional hardware, such as if I were to use LoRa for example. Although using wifi does consume more power, the advantages outweighs the disadvantages overall.

``` Python
def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
    
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        wlan.config(pm = 0xa11140)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
            
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip
```
Additionally, the **MQTT protocol** is used to deliver to Adafruit IO since it is fast, efficient and ideal for Iot projects. Furthermore, **Webhook** is used to trigger an action for sending a message through discord when the trash is in it's maximum capacity.

``` Python
def connect(self):
    """Connect to Adafruit IO"""
    try:
        self.client = MQTTClient(
            client_id="smart-trashcan-" + config.AIO_USER,
            server=config.AIO_SERVER,
            user=config.AIO_USER,
            password=config.AIO_KEY,
            port=config.AIO_PORT
        )
        self.client.connect()
        self.connected = True
```

## :bar_chart: Presenting the data
I used the free version of Adafruit IO so the data is saved for 30 days before it erases itself.
![Screenshot 2025-06-30 at 16.19.07](https://hackmd.io/_uploads/S10iTMxBle.png)

I also added an action in Adafruit IO to sent a message through my own discord server whenever the trash is full.
![Screenshot 2025-06-24 at 11.30.08](https://hackmd.io/_uploads/SJb_exd4gg.png)

## :sparkler: Finalizing the design
:::info
:clapper: Video demonstration: https://youtu.be/JLW9DjHuwIo 
:::
Overall, I am satisfied with the outcome of my project and while the physical appearance doesn't necessarily meet my standards and could be improved, I believe that the main functionalities is the most important part which works as it should and does meet my expectations.

If I had more time and resources, I would have definitely focused more on the design aspect of it, particularly by using a 3d-printer however I do not have access to one, which limited the overall appearance as I'm not very good with designing handmade things. Additionally, I had several more ideas that i would have explored to make the smart trashcan more optimal, effective and inclusive. Such as a multi-level detectection system for fullness, height-adjustable lid mechanism, having recycling sorting and maybe for fun, having an LCD display.

I am proud of what I've achieved in this project and I genuinely believe I put on my best effort throughout this whole process. I challenged myself, learned new skills and I'm happy with the final result.

![ActualProjectpicture](https://hackmd.io/_uploads/SyoXibxHll.jpg)

![insideProject_11zon-2](https://hackmd.io/_uploads/Hks-3-xrle.jpg)
