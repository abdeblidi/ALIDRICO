from django.core.management.base import BaseCommand
from catalog.models import Category, Product, Specification


class Command(BaseCommand):
    help = 'Seed the database with sample electronic components'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create Categories
        categories_data = [
            {"name": "Diodes", "slug": "diodes", "icon": "bi-diagram-2", "description": "General purpose, Schottky, Zener, LED and power diodes"},
            {"name": "Resistors", "slug": "resistors", "icon": "bi-resistor", "description": "Fixed, variable, SMD and resistor networks"},
            {"name": "Capacitors", "slug": "capacitors", "icon": "bi-battery", "description": "Ceramic, electrolytic, tantalum and film capacitors"},
            {"name": "Transistors", "slug": "transistors", "icon": "bi-cpu", "description": "NPN, PNP, MOSFET, IGBT and JFET transistors"},
            {"name": "LEDs", "slug": "leds", "icon": "bi-lightbulb", "description": "Various colors, RGB, SMD, high power and LED strips"},
            {"name": "Integrated Circuits", "slug": "integrated-circuits", "icon": "bi-motherboard", "description": "ICs, voltage regulators, op-amps and converters"},
            {"name": "Arduino / ESP32", "slug": "arduino-esp32", "icon": "bi-usb-symbol", "description": "Arduino boards, ESP32, WiFi/Bluetooth modules"},
            {"name": "Microcontrollers", "slug": "microcontrollers", "icon": "bi-chip", "description": "AVR, PIC, ARM, STM32 and TI microcontrollers"},
            {"name": "Connectors", "slug": "connectors", "icon": "bi-plugin", "description": "Connectors, sockets, pin headers and terminals"},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_data["name"],
                    "icon": cat_data["icon"],
                    "description": cat_data["description"],
                    "is_active": True
                }
            )
            categories[cat_data["slug"]] = cat
            action = "Created" if created else "Exists"
            self.stdout.write(f"  {action}: {cat.name}")

        # Create Products
        products_data = [
            # Diodes
            {"name": "1N4007 Diode", "part_number": "1N4007", "category": "diodes",
             "description": "General purpose rectifier diode. 1000V 1A. Ideal for rectification and reverse current protection applications.",
             "short_description": "General purpose rectifier diode 1000V 1A", "is_featured": True},
            {"name": "1N4001 Diode", "part_number": "1N4001", "category": "diodes",
             "description": "General purpose rectifier diode. 50V 1A. Suitable for low voltage circuits.",
             "short_description": "General purpose diode 50V 1A", "is_featured": False},
            {"name": "1N5408 Diode", "part_number": "1N5408", "category": "diodes",
             "description": "High power rectifier diode. 1000V 3A. Suitable for high power rectification applications.",
             "short_description": "High power diode 1000V 3A", "is_featured": False},
            {"name": "1N5819 Schottky Diode", "part_number": "1N5819", "category": "diodes",
             "description": "Schottky barrier diode. 40V 1A. Low forward voltage drop ideal for fast switching applications.",
             "short_description": "Schottky diode 40V 1A", "is_featured": True},
            {"name": "FR107 Fast Recovery", "part_number": "FR107", "category": "diodes",
             "description": "Fast recovery rectifier diode. 1000V 1A. Ideal for high frequency applications.",
             "short_description": "Fast recovery diode 1000V 1A", "is_featured": False},
            {"name": "1N4148 Signal Diode", "part_number": "1N4148", "category": "diodes",
             "description": "High speed signal diode. 100V 200mA. Most commonly used in digital and switching circuits.",
             "short_description": "Signal diode 100V 200mA", "is_featured": True},

            # Resistors
            {"name": "10kΩ Resistor", "part_number": "10K-1/4W", "category": "resistors",
             "description": "10 kilo-ohm 1/4 watt 5% carbon film resistor. Most commonly used in electronic circuits.",
             "short_description": "10kΩ 1/4W 5% resistor", "is_featured": True},
            {"name": "1kΩ Resistor", "part_number": "1K-1/4W", "category": "resistors",
             "description": "1 kilo-ohm 1/4 watt 5% carbon film resistor. Standard through-hole resistor.",
             "short_description": "1kΩ 1/4W 5% resistor", "is_featured": False},
            {"name": "100Ω Resistor", "part_number": "100R-1/4W", "category": "resistors",
             "description": "100 ohm 1/4 watt 5% carbon film resistor. Used for current limiting applications.",
             "short_description": "100Ω 1/4W 5% resistor", "is_featured": False},
            {"name": "220Ω Resistor", "part_number": "220R-1/4W", "category": "resistors",
             "description": "220 ohm 1/4 watt 5% carbon film resistor. Common for LED current limiting.",
             "short_description": "220Ω 1/4W 5% resistor", "is_featured": True},

            # Capacitors
            {"name": "100µF Capacitor", "part_number": "100uF-25V", "category": "capacitors",
             "description": "100 microfarad 25V electrolytic capacitor. Ideal for power supply filtering and decoupling.",
             "short_description": "100µF 25V electrolytic capacitor", "is_featured": True},
            {"name": "10µF Capacitor", "part_number": "10uF-50V", "category": "capacitors",
             "description": "10 microfarad 50V electrolytic capacitor. General purpose filtering capacitor.",
             "short_description": "10µF 50V electrolytic capacitor", "is_featured": False},
            {"name": "100nF Ceramic", "part_number": "100nF-50V", "category": "capacitors",
             "description": "100 nanofarad 50V ceramic disc capacitor. Used for high frequency decoupling.",
             "short_description": "100nF 50V ceramic capacitor", "is_featured": True},
            {"name": "470µF Capacitor", "part_number": "470uF-16V", "category": "capacitors",
             "description": "470 microfarad 16V electrolytic capacitor. Large value for power supply smoothing.",
             "short_description": "470µF 16V electrolytic capacitor", "is_featured": False},

            # Transistors
            {"name": "BC547 Transistor", "part_number": "BC547", "category": "transistors",
             "description": "NPN general purpose transistor. Popular for switching and amplification circuits.",
             "short_description": "NPN transistor for general purpose", "is_featured": True},
            {"name": "BC557 Transistor", "part_number": "BC557", "category": "transistors",
             "description": "PNP general purpose transistor. Complementary to BC547.",
             "short_description": "PNP transistor for general purpose", "is_featured": False},
            {"name": "2N2222 Transistor", "part_number": "2N2222", "category": "transistors",
             "description": "NPN switching transistor. 800mA collector current. High speed switching applications.",
             "short_description": "NPN switching transistor 800mA", "is_featured": True},
            {"name": "2N3904 Transistor", "part_number": "2N3904", "category": "transistors",
             "description": "NPN general purpose amplifier. 200mA collector current. TO-92 package.",
             "short_description": "NPN amplifier transistor 200mA", "is_featured": False},

            # LEDs
            {"name": "Red LED 5mm", "part_number": "LED-5MM-R", "category": "leds",
             "description": "Red 5mm LED high brightness. 20mA forward current. 620-625nm wavelength.",
             "short_description": "Red LED 5mm high brightness", "is_featured": True},
            {"name": "Green LED 5mm", "part_number": "LED-5MM-G", "category": "leds",
             "description": "Green 5mm LED high brightness. 20mA forward current. 520-525nm wavelength.",
             "short_description": "Green LED 5mm high brightness", "is_featured": False},
            {"name": "Blue LED 5mm", "part_number": "LED-5MM-B", "category": "leds",
             "description": "Blue 5mm LED high brightness. 20mA forward current. 460-465nm wavelength.",
             "short_description": "Blue LED 5mm high brightness", "is_featured": True},
            {"name": "RGB LED 5mm", "part_number": "LED-5MM-RGB", "category": "leds",
             "description": "Common cathode RGB LED 5mm. 4-pin through-hole package. Mix colors for any output.",
             "short_description": "RGB LED 5mm common cathode", "is_featured": False},

            # Microcontrollers
            {"name": "ATmega328P", "part_number": "ATmega328P", "category": "microcontrollers",
             "description": "8-bit AVR microcontroller. 32KB flash, 2KB SRAM, 1KB EEPROM. Used in Arduino UNO.",
             "short_description": "8-bit AVR microcontroller 32KB", "is_featured": True},
            {"name": "ATtiny85", "part_number": "ATtiny85", "category": "microcontrollers",
             "description": "8-bit AVR tiny microcontroller. 8KB flash, 512B SRAM. 8-pin DIP package.",
             "short_description": "8-bit tiny AVR 8KB flash", "is_featured": False},
            {"name": "PIC16F877A", "part_number": "PIC16F877A", "category": "microcontrollers",
             "description": "8-bit PIC microcontroller. 14KB flash, 368B RAM. 40-pin DIP package.",
             "short_description": "8-bit PIC microcontroller 14KB", "is_featured": True},

            # Arduino / ESP32
            {"name": "Arduino UNO R3", "part_number": "ARD-UNO-R3", "category": "arduino-esp32",
             "description": "Arduino UNO R3 board with ATmega328P. USB cable included. Perfect for beginners.",
             "short_description": "Arduino UNO R3 development board", "is_featured": True},
            {"name": "ESP32 DevKit", "part_number": "ESP32-DEVKIT", "category": "arduino-esp32",
             "description": "ESP32 development board with WiFi and Bluetooth. Dual core processor. 30 pins.",
             "short_description": "ESP32 WiFi/Bluetooth dev board", "is_featured": True},
            {"name": "Arduino Nano", "part_number": "ARD-NANO", "category": "arduino-esp32",
             "description": "Arduino Nano board with ATmega328P. Compact size with USB Mini. Breadboard friendly.",
             "short_description": "Arduino Nano compact board", "is_featured": False},

            # ICs
            {"name": "LM7805 Regulator", "part_number": "LM7805", "category": "integrated-circuits",
             "description": "5V positive voltage regulator. 1.5A output current. TO-220 package. Input up to 35V.",
             "short_description": "5V voltage regulator 1.5A", "is_featured": True},
            {"name": "LM317 Regulator", "part_number": "LM317", "category": "integrated-circuits",
             "description": "Adjustable voltage regulator. 1.5A output. 1.25V to 37V adjustable output.",
             "short_description": "Adjustable voltage regulator", "is_featured": False},
            {"name": "NE555 Timer", "part_number": "NE555", "category": "integrated-circuits",
             "description": "Precision timer IC. Astable and monostable modes. DIP-8 package.",
             "short_description": "Precision timer IC DIP-8", "is_featured": True},
            {"name": "LM358 Op-Amp", "part_number": "LM358", "category": "integrated-circuits",
             "description": "Dual operational amplifier. Low power. DIP-8 package. Single supply operation.",
             "short_description": "Dual op-amp low power DIP-8", "is_featured": False},

            # Connectors
            {"name": "Male Pin Header", "part_number": "HDR-M-40", "category": "connectors",
             "description": "40-pin male pin header strip. 2.54mm pitch. Breakable into smaller sections.",
             "short_description": "40-pin male header 2.54mm", "is_featured": True},
            {"name": "Female Pin Header", "part_number": "HDR-F-40", "category": "connectors",
             "description": "40-pin female pin header strip. 2.54mm pitch. For breadboard connections.",
             "short_description": "40-pin female header 2.54mm", "is_featured": False},
        ]

        for prod_data in products_data:
            cat_slug = prod_data.pop("category")
            category = categories.get(cat_slug)
            if not category:
                continue

            prod, created = Product.objects.get_or_create(
                part_number=prod_data["part_number"],
                defaults={
                    "name": prod_data["name"],
                    "category": category,
                    "description": prod_data["description"],
                    "short_description": prod_data["short_description"],
                    "is_featured": prod_data["is_featured"],
                    "is_active": True
                }
            )
            action = "Created" if created else "Exists"
            self.stdout.write(f"  {action}: {prod.name}")

        # Add specifications to some products
        specs_data = {
            "1N4007": [
                ("Type", "Rectifier Diode"),
                ("Max Reverse Voltage", "1000V"),
                ("Forward Current", "1.0A"),
                ("Forward Voltage", "1.1V @ 1A"),
                ("Reverse Current", "5µA @ 1000V"),
                ("Package", "DO-41"),
                ("Operating Temp", "-55°C to +175°C"),
            ],
            "BC547": [
                ("Type", "NPN Transistor"),
                ("VCEO", "45V"),
                ("IC Max", "100mA"),
                ("hFE", "110-800"),
                ("Package", "TO-92"),
                ("Power Dissipation", "500mW"),
            ],
            "ATmega328P": [
                ("Architecture", "8-bit AVR"),
                ("Flash Memory", "32KB"),
                ("SRAM", "2KB"),
                ("EEPROM", "1KB"),
                ("Clock Speed", "16MHz"),
                ("Operating Voltage", "1.8V - 5.5V"),
                ("GPIO Pins", "23"),
            ],
            "10K-1/4W": [
                ("Resistance", "10kΩ"),
                ("Power Rating", "1/4W"),
                ("Tolerance", "±5%"),
                ("Type", "Carbon Film"),
                ("Package", "Through-Hole"),
            ],
            "100uF-25V": [
                ("Capacitance", "100µF"),
                ("Voltage Rating", "25V"),
                ("Type", "Electrolytic"),
                ("Tolerance", "±20%"),
                ("Package", "Radial"),
            ],
        }

        for part_num, specs in specs_data.items():
            try:
                product = Product.objects.get(part_number=part_num)
                for name, value in specs:
                    Specification.objects.get_or_create(
                        product=product,
                        name=name,
                        defaults={"value": value}
                    )
                self.stdout.write(f"  Added specs: {product.name}")
            except Product.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
