import spidev
import time

# Define OLED parameters
WIDTH = 128
HEIGHT = 64
SPI_PORT = 0
SPI_DEVICE = 0

# Function to send command to OLED
def command(spi, cmd):
    spi.xfer2([0x00, cmd])

# Function to send data to OLED
def data(spi, data):
    spi.xfer2([0x40, data])

# Function to initialize OLED
def init_display():
    spi = spidev.SpiDev()
    spi.open(SPI_PORT, SPI_DEVICE)
    spi.max_speed_hz = 5000000  # Set SPI speed to 5MHz (adjust if needed)

    # Send initialization commands
    command(spi, 0xAE)  # Display off
    command(spi, 0xD5)  # Set display clock divide ratio/oscillator frequency
    command(spi, 0x80)  # Default
    command(spi, 0xA8)  # Set multiplex ratio
    command(spi, HEIGHT - 1)
    command(spi, 0xD3)  # Set display offset
    command(spi, 0x00)  # Default
    command(spi, 0x40)  # Set display start line
    command(spi, 0x8D)  # Charge pump setting
    command(spi, 0x14)  # Enable charge pump
    command(spi, 0x20)  # Set memory addressing mode
    command(spi, 0x00)  # Horizontal addressing mode
    command(spi, 0xA1)  # Set segment remap
    command(spi, 0xC8)  # Set COM output scan direction
    command(spi, 0xDA)  # Set COM pins hardware configuration
    command(spi, 0x12)  # Default
    command(spi, 0x81)  # Set contrast control
    command(spi, 0xCF)  # Default
    command(spi, 0xD9)  # Set pre-charge period
    command(spi, 0xF1)  # Default
    command(spi, 0xDB)  # Set VCOMH deselect level
    command(spi, 0x40)  # Default
    command(spi, 0xA4)  # Set entire display on/off
    command(spi, 0xA6)  # Set normal display
    command(spi, 0xAF)  # Display on

    return spi

# Function to clear the display
def clear_display(spi):
    for page in range(8):
        command(spi, 0xB0 + page)  # Set page address
        command(spi, 0x00)  # Set lower column address
        command(spi, 0x10)  # Set higher column address
        for column in range(WIDTH):
            data(spi, 0x00)  # Clear each column

# Function to display a character
def display_char(spi, char):
    for i in range(8):
        command(spi, 0xB0 + i)  # Set page address
        command(spi, 0x00)  # Set lower column address
        command(spi, 0x10)  # Set higher column address
        for j in range(16):
            data(spi, font[char*16 + i*2 + j])  # Display character

# Define font data for ASCII characters (5x8 font)
font = [
    0x00, 0x00, 0x00, 0x00, 0x00,  # (space)
    # Define font data for other characters as needed...
    # Example: font data for "A"
    0x00, 0x7E, 0x11, 0x11, 0x7E,  # A
]

def main():
    spi = init_display()
    clear_display(spi)
    display_char(spi, ord('A'))
    time.sleep(5)  # Display "A" for 5 seconds
    spi.close()  # Close SPI connection

if __name__ == "__main__":
    main()

