## Flashing device

Requires `esptool`

`pip install esptool`

Commands to flash

```bash
esptool --port COM6 erase_flash
esptool --port COM6 write_flash --flash_size=detect -fm dio 0x00000 ESP8266_GENERIC-20240602-v1.23.0.bin
```

## Copying files

requires `adafruit-ampy`

`pip install adafruit-ampy`

List remote files
`  ampy --port COM6 ls`
